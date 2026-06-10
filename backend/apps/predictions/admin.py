from django.contrib import admin
from apps.predictions.models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ("match", "predictor_type", "predicted_score_a", "predicted_score_b", "confidence_score")
    list_filter = ("predictor_type",)
    search_fields = ("match__team_a__name", "match__team_b__name")
