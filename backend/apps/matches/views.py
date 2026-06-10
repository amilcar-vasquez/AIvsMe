from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.matches.models import Match
from apps.matches.serializers import MatchSerializer, SetResultSerializer
from apps.predictions.models import Prediction
from apps.scoreboard.services import recalculate_scoreboard
from services.ai_prediction_engine import generate_prediction


class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Match.objects.select_related("team_a", "team_b").all()
    serializer_class = MatchSerializer

    @action(detail=False, methods=["get"], url_path="upcoming")
    def upcoming(self, request):
        queryset = self.get_queryset().filter(status=Match.Status.UPCOMING)
        return Response(self.get_serializer(queryset, many=True).data)

    @action(detail=False, methods=["get"], url_path="completed")
    def completed(self, request):
        queryset = self.get_queryset().filter(status=Match.Status.COMPLETED)
        return Response(self.get_serializer(queryset, many=True).data)

    @action(detail=True, methods=["post"], url_path="set-result")
    def set_result(self, request, pk=None):
        match = self.get_object()
        serializer = SetResultSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        match.actual_score_a = serializer.validated_data["actual_score_a"]
        match.actual_score_b = serializer.validated_data["actual_score_b"]
        match.status = Match.Status.COMPLETED
        match.save(update_fields=["actual_score_a", "actual_score_b", "status"])

        if not Prediction.objects.filter(match=match, predictor_type=Prediction.PredictorType.AI).exists():
            generated = generate_prediction(match.team_a, match.team_b)
            Prediction.objects.create(
                match=match,
                predictor_type=Prediction.PredictorType.AI,
                predicted_score_a=generated.score_a,
                predicted_score_b=generated.score_b,
                confidence_score=generated.confidence,
                reasoning=generated.reasoning,
            )

        scoreboard = recalculate_scoreboard()
        payload = {
            "match": MatchSerializer(match).data,
            "scoreboard": {
                "total_matches": scoreboard.total_matches,
                "human_points": scoreboard.human_points,
                "ai_points": scoreboard.ai_points,
                "human_exact_scores": scoreboard.human_exact_scores,
                "ai_exact_scores": scoreboard.ai_exact_scores,
            },
        }
        return Response(payload, status=status.HTTP_200_OK)
