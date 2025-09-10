from django.contrib import admin
from .models import Team, Game, Odds


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "conference", "division")
    search_fields = ("name",)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "season", "week", "home_team", "away_team", "kickoff", "venue", "roof")
    list_filter = ("season", "week", "venue", "roof")
    search_fields = ("home_team__name", "away_team__name")
    autocomplete_fields = ("home_team", "away_team")


@admin.register(Odds)
class OddsAdmin(admin.ModelAdmin):
    list_display = ("id", "game", "book", "spread", "spread_price", "total", "total_price", "moneyline_home", "moneyline_away", "captured_at")
    list_filter = ("book",)
    search_fields = ("book", "game__home_team__name", "game__away_team__name")