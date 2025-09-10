from django.core.management.base import BaseCommand
from django.utils import timezone
from games.models import Team, Game, Odds


class Command(BaseCommand):
    help = "Seed demo teams, a game, and odds"

    def handle(self, *args, **kwargs):
        eagles, _ = Team.objects.get_or_create(name="Eagles", conference="NFC", division="East")
        cowboys, _ = Team.objects.get_or_create(name="Cowboys", conference="NFC", division="East")

        g = Game.objects.create(
            season=2025, week=1,
            home_team=eagles, away_team=cowboys,
            kickoff=timezone.now(),
            venue="Lincoln Financial Field", roof="outdoor"
        )

        Odds.objects.create(
            game=g, book="DemoBook",
            spread=-3.5, spread_price=-110,
            total=47.5, total_price=-110,
            moneyline_home=-160, moneyline_away=140
        )

        self.stdout.write(self.style.SUCCESS("Seeded demo data."))
