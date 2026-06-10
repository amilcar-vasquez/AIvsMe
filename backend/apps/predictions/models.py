import uuid
from django.db import models
from apps.matches.models import Match


class Prediction(models.Model):
    class PredictorType(models.TextChoices):
        HUMAN = "human", "Human"
        AI = "ai", "AI"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="predictions")
    predictor_type = models.CharField(max_length=10, choices=PredictorType.choices)
    predicted_score_a = models.PositiveIntegerField()
    predicted_score_b = models.PositiveIntegerField()
    confidence_score = models.FloatField(default=50.0)
    reasoning = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("match", "predictor_type")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.predictor_type} -> {self.match}"
