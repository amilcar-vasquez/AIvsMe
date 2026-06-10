from django.contrib import admin
from apps.matches.models import Match
from apps.scoreboard.services import recalculate_scoreboard


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("team_a", "team_b", "stage", "status", "kickoff_time")
    list_filter = ("stage", "status")
    search_fields = ("team_a__name", "team_b__name", "stadium")
    actions = ["publish_results_and_recompute"]

    @admin.action(description="Publish results and recompute scoreboard")
    def publish_results_and_recompute(self, request, queryset):
        publishable = queryset.filter(
            actual_score_a__isnull=False,
            actual_score_b__isnull=False,
        ).exclude(status=Match.Status.COMPLETED)

        updated = publishable.update(status=Match.Status.COMPLETED)
        scoreboard = recalculate_scoreboard()

        self.message_user(
            request,
            (
                f"Published {updated} matches. "
                f"Scoreboard now Human {scoreboard.human_points} - AI {scoreboard.ai_points}."
            ),
        )
