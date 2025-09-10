from rest_framework import viewsets
from .models import Prediction
from .serializers import PredictionSerializer


class PredictionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PredictionSerializer

    def get_queryset(self):
        qs = Prediction.objects.select_related("game", "game__home_team", "game__away_team")
        game_id = self.request.query_params.get("game_id")
        if game_id:
            qs = qs.filter(game_id=game_id)
        return qs.order_by("-generated_at")