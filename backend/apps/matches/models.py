import uuid
from django.db import models
from apps.teams.models import Team


class Match(models.Model):
    class Stage(models.TextChoices):
        GROUP = "group", "Group"
        ROUND_OF_16 = "round_of_16", "Round of 16"
        QUARTERFINAL = "quarterfinal", "Quarterfinal"
        SEMIFINAL = "semifinal", "Semifinal"
        THIRD_PLACE = "third_place", "Third Place"
        FINAL = "final", "Final"

    class Status(models.TextChoices):
        UPCOMING = "upcoming", "Upcoming"
        LIVE = "live", "Live"
        COMPLETED = "completed", "Completed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="home_matches")
    team_b = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="away_matches")
    kickoff_time = models.DateTimeField()
    stadium = models.CharField(max_length=120, blank=True)
    stage = models.CharField(max_length=24, choices=Stage.choices, default=Stage.GROUP)
    actual_score_a = models.PositiveIntegerField(null=True, blank=True)
    actual_score_b = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.UPCOMING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["kickoff_time"]

    def __str__(self) -> str:
        return f"{self.team_a.country_code} vs {self.team_b.country_code}"
