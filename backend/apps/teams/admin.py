from django.contrib import admin
from apps.teams.models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "country_code", "fifa_rank", "group")
    search_fields = ("name", "country_code")
