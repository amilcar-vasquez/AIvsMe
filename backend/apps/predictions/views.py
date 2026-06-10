from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from apps.matches.models import Match
from apps.predictions.models import Prediction
from apps.predictions.serializers import PredictionSerializer
from services.ai_prediction_engine import generate_prediction


class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Prediction.objects.select_related("match", "match__team_a", "match__team_b").all()
    serializer_class = PredictionSerializer

    def perform_create(self, serializer):
        prediction = serializer.save()
        if prediction.predictor_type == Prediction.PredictorType.HUMAN:
            ai_exists = Prediction.objects.filter(
                match=prediction.match,
                predictor_type=Prediction.PredictorType.AI,
            ).exists()
            if not ai_exists:
                generated = generate_prediction(prediction.match.team_a, prediction.match.team_b)
                Prediction.objects.create(
                    match=prediction.match,
                    predictor_type=Prediction.PredictorType.AI,
                    predicted_score_a=generated.score_a,
                    predicted_score_b=generated.score_b,
                    confidence_score=generated.confidence,
                    reasoning=generated.reasoning,
                )


class MatchPredictionsViewSet(viewsets.ViewSet):
    def list(self, request, match_id=None):
        match = get_object_or_404(Match, id=match_id)
        queryset = Prediction.objects.filter(match=match).order_by("predictor_type")
        return Response(PredictionSerializer(queryset, many=True).data)
