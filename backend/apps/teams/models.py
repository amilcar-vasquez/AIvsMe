import uuid
from django.db import models


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=3, unique=True)
    fifa_rank = models.PositiveIntegerField()
    group = models.CharField(max_length=8, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["fifa_rank", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.country_code})"
