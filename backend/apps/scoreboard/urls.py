from django.urls import path
from apps.scoreboard.views import ScoreboardSocialCardView, ScoreboardView

urlpatterns = [
    path("scoreboard/", ScoreboardView.as_view(), name="scoreboard"),
    path("scoreboard/social-card/", ScoreboardSocialCardView.as_view(), name="scoreboard-social-card"),
]
