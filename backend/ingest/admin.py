from django.contrib import admin
from .models import Provider, RawGameSnapshot, RawOddsSnapshot, TeamAlias


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(RawGameSnapshot)
class RawGameSnapshotAdmin(admin.ModelAdmin):
    list_display = ("provider", "captured_at")
    list_filter = ("provider",)
    ordering = ("-captured_at",)


@admin.register(RawOddsSnapshot)
class RawOddsSnapshotAdmin(admin.ModelAdmin):
    list_display = ("provider", "captured_at")
    list_filter = ("provider",)
    ordering = ("-captured_at",)


@admin.register(TeamAlias)
class TeamAliasAdmin(admin.ModelAdmin):
    list_display = ("provider", "alias", "team_name")
    list_filter = ("provider",)
    search_fields = ("alias", "team_name")
