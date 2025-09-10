from rest_framework import serializers
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


