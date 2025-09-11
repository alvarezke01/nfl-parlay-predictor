from rest_framework import serializers
from betting.utils import (
    implied_prob_from_american, fair_american_from_prob,
    american_to_decimal, decimal_to_american
)
from .models import Parlay, ParlayLeg


class ParlayLegInputSerializer(serializers.Serializer):
    model_prob = serializers.FloatField(min_value=0.0, max_value=1.0)
    market_odds_american = serializers.IntegerField()
    # Optional future fields: leg_type, game_id, player_name, prop_type, line, side


class ParlayEvaluateRequestSerializer(serializers.Serializer):
    legs = ParlayLegInputSerializer(many=True)
    stake = serializers.FloatField(min_value=0.0, default=10.0)


class ParlayLegOutputSerializer(serializers.Serializer):
    model_prob = serializers.FloatField()
    fair_odds_american = serializers.IntegerField()
    market_odds_american = serializers.IntegerField()
    market_implied_prob = serializers.FloatField()
    leg_ev_at_1u = serializers.FloatField()


class ParlayEvaluateResponseSerializer(serializers.Serializer):
    legs = ParlayLegOutputSerializer(many=True)
    combined_probability = serializers.FloatField()
    fair_parlay_odds_american = serializers.IntegerField()
    market_parlay_odds_american = serializers.IntegerField()
    stake = serializers.FloatField()
    expected_payout = serializers.FloatField()
    expected_value = serializers.FloatField()


# Read-only model serializers for persisted Parlays
class ParlayLegModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParlayLeg
        fields = "__all__"


class ParlayModelSerializer(serializers.ModelSerializer):
    legs = ParlayLegModelSerializer(many=True, read_only=True)

    class Meta:
        model = Parlay
        fields = "__all__"


class ParlayCreateSerializer(serializers.Serializer):
    legs = ParlayLegInputSerializer(many=True)
    stake = serializers.FloatField(min_value=0.0, default=10.0)

    def create(self, validated_data):
        legs_data = validated_data["legs"]
        stake = validated_data["stake"]

        if not legs_data:
            raise serializers.ValidationError("At least one leg is required.")

        # Compute combined probability and market parlay decimal
        combined_prob = 1.0
        market_parlay_decimal = 1.0

        for leg in legs_data:
            p = float(leg["model_prob"])
            mkt = int(leg["market_odds_american"])
            mkt_dec = american_to_decimal(mkt)
            combined_prob *= p
            market_parlay_decimal *= mkt_dec

        # Create Parlay
        fair_parlay_american = fair_american_from_prob(combined_prob)
        market_parlay_american = decimal_to_american(market_parlay_decimal)
        expected_payout = stake * (market_parlay_decimal - 1.0)
        expected_value = (combined_prob * expected_payout) - ((1.0 - combined_prob) * stake)

        parlay = Parlay.objects.create(
            source="user",
            stake=stake,
            combined_probability=combined_prob,
            fair_odds_american=fair_parlay_american,
            market_parlay_odds_american=market_parlay_american,
            expected_value=expected_value,
        )

        # Create ParlayLegs
        for leg in legs_data:
            p = float(leg["model_prob"])
            mkt = int(leg["market_odds_american"])
            fair = fair_american_from_prob(p)
            mkt_dec = american_to_decimal(mkt)
            leg_ev_1u = (p * (mkt_dec - 1.0)) - ((1.0 - p) * 1.0)

            ParlayLeg.objects.create(
                parlay=parlay,
                leg_type="moneyline",  # Default for now
                model_prob=p,
                market_odds_american=mkt,
                leg_ev_at_1u=leg_ev_1u,
            )

        return parlay


