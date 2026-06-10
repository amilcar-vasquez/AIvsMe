from rest_framework import serializers
from apps.scoreboard.models import Scoreboard


class ScoreboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scoreboard
        fields = [
            "id",
            "total_matches",
            "human_points",
            "ai_points",
            "human_exact_scores",
            "ai_exact_scores",
            "last_updated",
        ]
