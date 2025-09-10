from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Team, Game, Odds
from .serializers import TeamSerializer, GameSerializer, OddsSerializer


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(name="season", type=int, required=False, location=OpenApiParameter.QUERY,
                         description="Filter by season, e.g., 2025"),
        OpenApiParameter(name="week", type=int, required=False, location=OpenApiParameter.QUERY,
                         description="Filter by week number, e.g., 1"),
    ]
)
class GameViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GameSerializer

    def get_queryset(self):
        season = self.request.query_params.get("season")
        week = self.request.query_params.get("week")
        qs = Game.objects.select_related("home_team", "away_team")
        if season:
            qs = qs.filter(season=season)
        if week:
            qs = qs.filter(week=week)
        return qs.order_by("kickoff")


@extend_schema(
    parameters=[
        OpenApiParameter(name="game_id", type=int, required=False, location=OpenApiParameter.QUERY,
                         description="Filter by Game ID"),
    ]
)
class OddsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OddsSerializer

    def get_queryset(self):
        game_id = self.request.query_params.get("game_id")
        qs = Odds.objects.all()
        if game_id:
            qs = qs.filter(game_id=game_id)
        return qs.order_by("-captured_at")