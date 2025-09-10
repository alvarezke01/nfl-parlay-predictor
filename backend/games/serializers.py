from rest_framework import serializers
from .models import Team, Game, Odds


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"


class GameSerializer(serializers.ModelSerializer):
    # Convenience read-only fields so clients don't need another call for names
    home = serializers.CharField(source="home_team.name", read_only=True)
    away = serializers.CharField(source="away_team.name", read_only=True)

    class Meta:
        model = Game
        fields = [
            "id", "season", "week", "home_team", "away_team", "home", "away",
            "kickoff", "venue", "roof", "weather_temp", "weather_wind"
        ]


class OddsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Odds
        fields = "__all__"
