from django.core.management.base import BaseCommand
from predictions.models import Prediction
from games.models import Game
import random


class Command(BaseCommand):
    help = "Write baseline predictions for a given season/week"

    def add_arguments(self, parser):
        parser.add_argument("--season", type=int, required=True)
        parser.add_argument("--week", type=int, required=True)

    def handle(self, *args, **opts):
        season, week = opts["season"], opts["week"]
        games = Game.objects.filter(season=season, week=week)

        if not games.exists():
            self.stdout.write(self.style.WARNING("No games found for that season/week."))
            return

        created = 0
        for g in games:
            p_home = 0.5 + random.uniform(-0.08, 0.08)
            p_home = max(0.05, min(0.95, p_home))
            Prediction.objects.create(
                game=g,
                model_version="v0.0-baseline",
                win_prob_home=p_home,
                win_prob_away=1 - p_home,
                expected_total=46.0 + random.uniform(-5, 5),
                spread_cover_home=0.5 + random.uniform(-0.1, 0.1),
                spread_cover_away=0.5 + random.uniform(-0.1, 0.1),
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Baseline predictions written for {created} game(s)."))
