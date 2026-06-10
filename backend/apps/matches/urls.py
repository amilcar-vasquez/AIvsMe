from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.matches.views import MatchViewSet

router = DefaultRouter()
router.register(r"matches", MatchViewSet, basename="matches")

urlpatterns = [
    path("", include(router.urls)),
]
