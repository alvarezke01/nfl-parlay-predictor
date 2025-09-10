from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, OpenApiExample
from betting.utils import (
    implied_prob_from_american, fair_american_from_prob,
    american_to_decimal, decimal_to_american
)
from .serializers import (
    ParlayEvaluateRequestSerializer,
    ParlayEvaluateResponseSerializer,
    ParlayModelSerializer,
)
from .models import Parlay


class ParlayEvaluateView(APIView):
    @extend_schema(
        tags=["parlay"],
        summary="Evaluate a parlay",
        description="Computes per-leg EV, combined probability, fair/market parlay odds, and EV for a stake. Assumes legs are independent (v1).",
        request=ParlayEvaluateRequestSerializer,
        responses=ParlayEvaluateResponseSerializer,
        examples=[OpenApiExample(
            "Three-leg parlay",
            value={
                "stake": 10,
                "legs": [
                    {"model_prob": 0.62, "market_odds_american": -140},
                    {"model_prob": 0.54, "market_odds_american": -110},
                    {"model_prob": 0.28, "market_odds_american": 200}
                ]
            }
        )]
    )
    def post(self, request):
        req = ParlayEvaluateRequestSerializer(data=request.data)
        req.is_valid(raise_exception=True)
        legs = req.validated_data["legs"]
        stake = req.validated_data["stake"]

        if not legs:
            return Response({"detail": "At least one leg is required."}, status=400)

        leg_outputs = []
        combined_prob = 1.0
        market_parlay_decimal = 1.0

        for leg in legs:
            p = float(leg["model_prob"])
            mkt = int(leg["market_odds_american"])
            fair = fair_american_from_prob(p)
            mkt_imp = implied_prob_from_american(mkt)
            mkt_dec = american_to_decimal(mkt)
            leg_ev_1u = (p * (mkt_dec - 1.0)) - ((1.0 - p) * 1.0)

            leg_outputs.append({
                "model_prob": round(p, 6),
                "fair_odds_american": fair,
                "market_odds_american": mkt,
                "market_implied_prob": round(mkt_imp, 6),
                "leg_ev_at_1u": round(leg_ev_1u, 6),
            })

            combined_prob *= p
            market_parlay_decimal *= mkt_dec

        fair_parlay_american = fair_american_from_prob(combined_prob)
        market_parlay_american = decimal_to_american(market_parlay_decimal)
        expected_payout = stake * (market_parlay_decimal - 1.0)
        expected_value = (combined_prob * expected_payout) - ((1.0 - combined_prob) * stake)

        return Response({
            "legs": leg_outputs,
            "combined_probability": round(combined_prob, 6),
            "fair_parlay_odds_american": fair_parlay_american,
            "market_parlay_odds_american": market_parlay_american,
            "stake": float(stake),
            "expected_payout": round(expected_payout, 2),
            "expected_value": round(expected_value, 2),
        })


class ParlayViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Parlay.objects.prefetch_related("legs").order_by("-created_at")
    serializer_class = ParlayModelSerializer


