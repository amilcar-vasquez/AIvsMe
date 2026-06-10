from rest_framework import serializers
from apps.matches.models import Match


class MatchSerializer(serializers.ModelSerializer):
    team_a_name = serializers.CharField(source="team_a.name", read_only=True)
    team_b_name = serializers.CharField(source="team_b.name", read_only=True)
    team_a_code = serializers.CharField(source="team_a.country_code", read_only=True)
    team_b_code = serializers.CharField(source="team_b.country_code", read_only=True)

    class Meta:
        model = Match
        fields = [
            "id",
            "team_a",
            "team_b",
            "team_a_name",
            "team_b_name",
            "team_a_code",
            "team_b_code",
            "kickoff_time",
            "stadium",
            "stage",
            "actual_score_a",
            "actual_score_b",
            "status",
            "created_at",
        ]


class SetResultSerializer(serializers.Serializer):
    actual_score_a = serializers.IntegerField(min_value=0)
    actual_score_b = serializers.IntegerField(min_value=0)
