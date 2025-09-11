from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from ingest.models import Provider, RawGameSnapshot, TeamAlias
from games.models import Team, Game
from dateutil import parser as dtp


class Command(BaseCommand):
    help = "Normalize the latest RawGameSnapshot (nfl_data_py) into Team and Game tables."

    def handle(self, *args, **options):
        provider = Provider.objects.get(name="nfl_data_py")
        snapshot = RawGameSnapshot.objects.filter(provider=provider).order_by("-captured_at").first()

        if not snapshot:
            self.stdout.write(self.style.WARNING("No RawGameSnapshot found for nfl_data_py."))
            return

        rows = snapshot.payload
        created_teams = 0
        created_games = 0

        # Build alias map to unify provider team names with canonical Team names.
        alias_map = {
            ta.alias.lower(): ta.team_name
            for ta in TeamAlias.objects.filter(provider=provider)
        }

        def canonical(name: str) -> str:
            return alias_map.get(name.lower(), name) if name else name

        with transaction.atomic():
            # Ensure all teams exist.
            team_names = set()
            for row in rows:
                team_names.add(canonical(row.get("home_team")))
                team_names.add(canonical(row.get("away_team")))

            for nm in sorted(filter(None, team_names)):
                _, created = Team.objects.get_or_create(
                    name=nm,
                    defaults={"conference": "", "division": ""},
                )
                if created:
                    created_teams += 1

            # Create or update games.
            for row in rows:
                season = int(row["season"])
                week = int(row["week"])
                home_name = canonical(row.get("home_team"))
                away_name = canonical(row.get("away_team"))
                if not home_name or not away_name:
                    continue

                try:
                    home_team = Team.objects.get(name=home_name)
                    away_team = Team.objects.get(name=away_name)
                except Team.DoesNotExist:
                    continue

                kickoff = None
                if row.get("gameday"):
                    naive_dt = dtp.parse(row["gameday"])
                    kickoff = timezone.make_aware(naive_dt)
                venue = row.get("stadium") or ""
                roof = row.get("roof") or ""

                obj, created = Game.objects.update_or_create(
                    season=season,
                    week=week,
                    home_team=home_team,
                    away_team=away_team,
                    defaults={
                        "kickoff": kickoff,
                        "venue": venue,
                        "roof": roof,
                    },
                )
                if created:
                    created_games += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Normalized {created_teams} new teams and {created_games} new games "
                f"from snapshot {snapshot.id}"
            )
        )
