from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from ingest.models import Provider, RawOddsSnapshot
import requests


class Command(BaseCommand):
    help = "Fetch current sportsbook odds JSON from the configured provider and store it."

    def add_arguments(self, parser):
        parser.add_argument(
            "--provider",
            type=str,
            default="odds_api",
            help="Logical provider name (default: odds_api)",
        )
        parser.add_argument(
            "--sport",
            type=str,
            default="americanfootball_nfl",
            help="Sport/league code understood by your provider",
        )

    def handle(self, *args, **opts):
        base = settings.ODDS_API_BASE
        key = settings.ODDS_API_KEY
        if not base or not key:
            raise CommandError("ODDS_API_BASE and ODDS_API_KEY must be set in .env")

        provider_name = opts["provider"]
        sport = opts["sport"]

        # Generic GET; adjust params to match your chosen odds provider's API
        # Example for The Odds API:
        #   GET {base}/sports/{sport}/odds?regions=us&markets=h2h,spreads,totals&apiKey=KEY
        url = f"{base}/sports/{sport}/odds"
        params = {
            "regions": "us",
            "markets": "h2h,spreads,totals",
            "apiKey": key,
        }

        self.stdout.write(f"Requesting odds from {url}")
        resp = requests.get(url, params=params, timeout=20)
        resp.raise_for_status()
        payload = resp.json()

        provider, _ = Provider.objects.get_or_create(name=provider_name)
        snap = RawOddsSnapshot.objects.create(provider=provider, payload=payload)
        self.stdout.write(self.style.SUCCESS(
            f"Stored RawOddsSnapshot id={snap.id} from provider={provider_name}, items={len(payload) if hasattr(payload,'__len__') else 'unknown'}"
        ))
