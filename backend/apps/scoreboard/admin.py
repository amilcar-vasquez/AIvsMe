from django.contrib import admin
from apps.scoreboard.models import Scoreboard
from apps.scoreboard.services import recalculate_scoreboard


@admin.register(Scoreboard)
class ScoreboardAdmin(admin.ModelAdmin):
    list_display = ("human_points", "ai_points", "total_matches", "last_updated")
    actions = ["recompute_scoreboard"]

    @admin.action(description="Recompute scoreboard now")
    def recompute_scoreboard(self, request, queryset):
        scoreboard = recalculate_scoreboard()
        self.message_user(
            request,
            (
                "Scoreboard recomputed: "
                f"Human {scoreboard.human_points} - AI {scoreboard.ai_points}, "
                f"Matches {scoreboard.total_matches}."
            ),
        )
