from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.predictions.views import MatchPredictionsViewSet, PredictionViewSet

router = DefaultRouter()
router.register(r"predictions", PredictionViewSet, basename="predictions")

match_predictions = MatchPredictionsViewSet.as_view({"get": "list"})

urlpatterns = [
    path("", include(router.urls)),
    path("matches/<uuid:match_id>/predictions/", match_predictions, name="match-predictions"),
]
