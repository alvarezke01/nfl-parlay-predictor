from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100)
    conference = models.CharField(max_length=10, blank=True)
    division = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    season = models.IntegerField()
    week = models.IntegerField()
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="home_games")
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="away_games")
    kickoff = models.DateTimeField()
    venue = models.CharField(max_length=100, blank=True)
    roof = models.CharField(max_length=20, blank=True)
    weather_temp = models.FloatField(null=True, blank=True)
    weather_wind = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.season} W{self.week}: {self.away_team} @ {self.home_team}"


class Odds(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="odds")
    book = models.CharField(max_length=50)
    spread = models.FloatField(null=True, blank=True)
    spread_price = models.IntegerField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)
    total_price = models.IntegerField(null=True, blank=True)
    moneyline_home = models.IntegerField(null=True, blank=True)
    moneyline_away = models.IntegerField(null=True, blank=True)
    captured_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["game", "book", "captured_at"])]