from django.contrib import admin
from .models import Parlay, ParlayLeg


class ParlayLegInline(admin.TabularInline):
    model = ParlayLeg
    extra = 0


@admin.register(Parlay)
class ParlayAdmin(admin.ModelAdmin):
    list_display = ("id", "source", "season", "week", "stake", "combined_probability", "fair_odds_american", "market_parlay_odds_american", "expected_value", "created_at")
    list_filter = ("source", "season", "week", "created_at")
    inlines = [ParlayLegInline]


@admin.register(ParlayLeg)
class ParlayLegAdmin(admin.ModelAdmin):
    list_display = ("id", "parlay", "leg_type", "game", "player_name", "prop_type", "line", "side", "model_prob", "market_odds_american", "leg_ev_at_1u")
    list_filter = ("leg_type", "prop_type")
    search_fields = ("player_name",)


