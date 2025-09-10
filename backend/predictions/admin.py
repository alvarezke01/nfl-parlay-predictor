from django.contrib import admin
from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ("id", "game", "model_version", "generated_at",
                    "win_prob_home", "win_prob_away",
                    "expected_total", "spread_cover_home", "spread_cover_away")
    list_filter = ("model_version", "generated_at")
    search_fields = ("game__home_team__name", "game__away_team__name", "model_version")