from rest_framework import serializers
from apps.predictions.models import Prediction


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = [
            "id",
            "match",
            "predictor_type",
            "predicted_score_a",
            "predicted_score_b",
            "confidence_score",
            "reasoning",
            "created_at",
        ]
