from apps.matches.models import Match
from apps.predictions.models import Prediction
from apps.scoreboard.models import Scoreboard


def _outcome(score_a: int, score_b: int) -> str:
    if score_a == score_b:
        return "draw"
    return "a" if score_a > score_b else "b"


def calculate_prediction_points(
    actual_score_a: int,
    actual_score_b: int,
    predicted_score_a: int,
    predicted_score_b: int,
) -> int:
    if actual_score_a == predicted_score_a and actual_score_b == predicted_score_b:
        return 3
    if _outcome(actual_score_a, actual_score_b) == _outcome(predicted_score_a, predicted_score_b):
        return 1
    return 0


def recalculate_scoreboard() -> Scoreboard:
    scoreboard, _ = Scoreboard.objects.get_or_create()

    completed = Match.objects.filter(
        status=Match.Status.COMPLETED,
        actual_score_a__isnull=False,
        actual_score_b__isnull=False,
    )

    human_points = 0
    ai_points = 0
    human_exact = 0
    ai_exact = 0

    for match in completed:
        predictions = {
            p.predictor_type: p
            for p in Prediction.objects.filter(match=match)
        }
        for predictor_type, prediction in predictions.items():
            points = calculate_prediction_points(
                match.actual_score_a,
                match.actual_score_b,
                prediction.predicted_score_a,
                prediction.predicted_score_b,
            )
            if predictor_type == Prediction.PredictorType.HUMAN:
                human_points += points
                if points == 3:
                    human_exact += 1
            elif predictor_type == Prediction.PredictorType.AI:
                ai_points += points
                if points == 3:
                    ai_exact += 1

    scoreboard.total_matches = completed.count()
    scoreboard.human_points = human_points
    scoreboard.ai_points = ai_points
    scoreboard.human_exact_scores = human_exact
    scoreboard.ai_exact_scores = ai_exact
    scoreboard.save()
    return scoreboard
