import uuid
from django.db import models


class Scoreboard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    total_matches = models.PositiveIntegerField(default=0)
    human_points = models.PositiveIntegerField(default=0)
    ai_points = models.PositiveIntegerField(default=0)
    human_exact_scores = models.PositiveIntegerField(default=0)
    ai_exact_scores = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Human {self.human_points} - AI {self.ai_points}"
