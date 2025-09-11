from django.db import models


class Provider(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class RawGameSnapshot(models.Model):
    """
    Append-only store of raw schedule/game payloads from a provider.
    Each row represents one capture (e.g., a full schedule dataframe as JSON).
    """
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    captured_at = models.DateTimeField(auto_now_add=True)
    payload = models.JSONField()

    class Meta:
        indexes = [
            models.Index(fields=["provider", "captured_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.provider} @ {self.captured_at:%Y-%m-%d %H:%M}"


class RawOddsSnapshot(models.Model):
    """
    Append-only store of raw odds payloads from a provider (to be normalized later).
    """
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    captured_at = models.DateTimeField(auto_now_add=True)
    payload = models.JSONField()

    class Meta:
        indexes = [
            models.Index(fields=["provider", "captured_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.provider} odds @ {self.captured_at:%Y-%m-%d %H:%M}"


class TeamAlias(models.Model):
    """
    Maps a provider's team name/alias to our canonical Team.name.
    This lets different sources resolve to the same Team.
    """
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    alias = models.CharField(max_length=100)
    team_name = models.CharField(max_length=100)  # canonical Team.name

    class Meta:
        unique_together = ("provider", "alias")
        indexes = [
            models.Index(fields=["provider", "alias"]),
        ]

    def __str__(self) -> str:
        return f"{self.provider}:{self.alias} -> {self.team_name}"
