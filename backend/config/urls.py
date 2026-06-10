from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.teams.urls")),
    path("api/", include("apps.matches.urls")),
    path("api/", include("apps.predictions.urls")),
    path("api/", include("apps.scoreboard.urls")),
]
