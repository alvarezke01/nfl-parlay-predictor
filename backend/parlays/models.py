from django.db import models
from games.models import Game


class Parlay(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=20, default="user")  # "user" | "ai"
    season = models.IntegerField(null=True, blank=True)
    week = models.IntegerField(null=True, blank=True)
    stake = models.FloatField(default=0.0)
    combined_probability = models.FloatField(null=True, blank=True)
    fair_odds_american = models.IntegerField(null=True, blank=True)
    market_parlay_odds_american = models.IntegerField(null=True, blank=True)
    expected_value = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Parlay #{self.id} ({self.source})"


class ParlayLeg(models.Model):
    parlay = models.ForeignKey(Parlay, on_delete=models.CASCADE, related_name="legs")
    leg_type = models.CharField(max_length=20)  # "moneyline"|"spread"|"total"|"prop"
    # References:
    game = models.ForeignKey(Game, null=True, blank=True, on_delete=models.SET_NULL)
    player_name = models.CharField(max_length=100, blank=True)
    prop_type = models.CharField(max_length=40, blank=True)  # e.g., "anytime_td", "receiving_yards"
    line = models.FloatField(null=True, blank=True)
    side = models.CharField(max_length=20, blank=True)  # "home","away","over","under"

    # Pricing & evaluation inputs/outputs
    model_prob = models.FloatField()
    market_odds_american = models.IntegerField()
    leg_ev_at_1u = models.FloatField(null=True, blank=True)

    def __str__(self):
        label = self.prop_type or self.leg_type
        return f"{label} {self.side or ''} {self.market_odds_american}".strip()


