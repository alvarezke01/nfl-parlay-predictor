from django.core.management.base import BaseCommand
from django.utils import timezone
from ingest.models import Provider, RawGameSnapshot
import nfl_data_py as nfl
import pandas as pd
import json


class Command(BaseCommand):
    help = "Backfill historical NFL schedules into RawGameSnapshot."

    def add_arguments(self, parser):
        parser.add_argument(
            "--seasons",
            type=str,
            required=True,
            help='Comma-separated seasons, e.g. "2023,2024,2025"',
        )

    def handle(self, *args, **options):
        seasons = [int(s.strip()) for s in options["seasons"].split(",") if s.strip()]
        provider, _ = Provider.objects.get_or_create(name="nfl_data_py")

        # Fetch schedule data as a DataFrame
        self.stdout.write(f"Fetching NFL schedules for seasons: {seasons}")
        df: pd.DataFrame = nfl.import_schedules(seasons)

        # Convert DataFrame to JSON-serializable format
        # Use pandas' built-in JSON conversion which handles NaN properly
        json_str = df.to_json(orient="records", date_format="iso")
        payload = json.loads(json_str)

        # Store a raw snapshot (append-only)
        snap = RawGameSnapshot.objects.create(provider=provider, payload=payload)

        self.stdout.write(
            self.style.SUCCESS(
                f"Stored RawGameSnapshot id={snap.id} with {len(payload)} games "
                f"for seasons {seasons} at {timezone.now():%Y-%m-%d %H:%M}"
            )
        )
