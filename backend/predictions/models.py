from django.db import models
from games.models import Game


class Prediction(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="predictions")
    model_version = models.CharField(max_length=20)
    generated_at = models.DateTimeField(auto_now_add=True)

    # Game-level outputs
    win_prob_home = models.FloatField()
    win_prob_away = models.FloatField()
    expected_total = models.FloatField()
    spread_cover_home = models.FloatField()
    spread_cover_away = models.FloatField()

    def __str__(self):
        return f"{self.game} | {self.model_version} @ {self.generated_at:%Y-%m-%d %H:%M}"