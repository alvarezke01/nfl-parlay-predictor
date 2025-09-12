from django.core.management.base import BaseCommand
from django.db import transaction
from ingest.models import Provider, RawOddsSnapshot, TeamAlias
from games.models import Team, Game, Odds
from django.utils import timezone


class Command(BaseCommand):
    help = "Normalize the latest RawOddsSnapshot into canonical games.Odds records."

    def add_arguments(self, parser):
        parser.add_argument(
            "--provider",
            type=str,
            default="odds_api",
            help="Provider name to normalize (default: odds_api)",
        )
        parser.add_argument(
            "--season",
            type=int,
            required=False,
            help="Optional: restrict normalization to a season",
        )
        parser.add_argument(
            "--week",
            type=int,
            required=False,
            help="Optional: restrict normalization to a week",
        )

    def handle(self, *args, **opts):
        provider = Provider.objects.get(name=opts["provider"])
        snap = (
            RawOddsSnapshot.objects.filter(provider=provider)
            .order_by("-captured_at")
            .first()
        )
        if not snap:
            self.stdout.write(self.style.WARNING("No RawOddsSnapshot found."))
            return

        alias_map = {
            ta.alias.lower(): ta.team_name
            for ta in TeamAlias.objects.filter(provider=provider)
        }

        def canonical(name: str) -> str:
            return alias_map.get(name.lower(), name) if name else name

        rows = snap.payload
        created = 0

        with transaction.atomic():
            for r in rows:
                # The Odds API structure: home_team, away_team, bookmakers[]
                home_name = canonical(r.get("home_team"))
                away_name = canonical(r.get("away_team"))
                
                if not home_name or not away_name:
                    continue

                try:
                    home = Team.objects.get(name=home_name)
                    away = Team.objects.get(name=away_name)
                except Team.DoesNotExist:
                    continue

                # Find matching game
                qs = Game.objects.filter(home_team=home, away_team=away)
                if opts.get("season"):
                    qs = qs.filter(season=opts["season"])
                if opts.get("week"):
                    qs = qs.filter(week=opts["week"])

                game = qs.order_by("-kickoff").first()
                if not game:
                    continue

                # Process each bookmaker
                for bookmaker in r.get("bookmakers", []):
                    book_name = bookmaker.get("title", "UNKNOWN")
                    
                    # Extract odds from different markets
                    spread = None
                    spread_price = None
                    total = None
                    total_price = None
                    moneyline_home = None
                    moneyline_away = None

                    for market in bookmaker.get("markets", []):
                        market_key = market.get("key")
                        outcomes = market.get("outcomes", [])

                        if market_key == "h2h":  # Moneyline
                            for outcome in outcomes:
                                if outcome.get("name") == home_name:
                                    # Convert decimal odds to American
                                    decimal_odds = outcome.get("price", 0)
                                    if decimal_odds > 0 and decimal_odds != 1:
                                        moneyline_home = int((decimal_odds - 1) * 100) if decimal_odds >= 2 else int(-100 / (decimal_odds - 1))
                                elif outcome.get("name") == away_name:
                                    decimal_odds = outcome.get("price", 0)
                                    if decimal_odds > 0 and decimal_odds != 1:
                                        moneyline_away = int((decimal_odds - 1) * 100) if decimal_odds >= 2 else int(-100 / (decimal_odds - 1))

                        elif market_key == "spreads":  # Point spreads
                            for outcome in outcomes:
                                if outcome.get("name") == home_name:
                                    spread = outcome.get("point")
                                    decimal_odds = outcome.get("price", 0)
                                    if decimal_odds > 0 and decimal_odds != 1:
                                        spread_price = int((decimal_odds - 1) * 100) if decimal_odds >= 2 else int(-100 / (decimal_odds - 1))
                                    break

                        elif market_key == "totals":  # Over/Under
                            for outcome in outcomes:
                                if outcome.get("name") == "Over":
                                    total = outcome.get("point")
                                    decimal_odds = outcome.get("price", 0)
                                    if decimal_odds > 0 and decimal_odds != 1:
                                        total_price = int((decimal_odds - 1) * 100) if decimal_odds >= 2 else int(-100 / (decimal_odds - 1))
                                    break

                    # Create Odds record
                    Odds.objects.create(
                        game=game,
                        book=book_name,
                        spread=spread,
                        spread_price=spread_price,
                        total=total,
                        total_price=total_price,
                        moneyline_home=moneyline_home,
                        moneyline_away=moneyline_away,
                        captured_at=timezone.now(),
                    )
                    created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {created} Odds records from snapshot {snap.id}"
            )
        )
