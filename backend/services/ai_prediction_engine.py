import hashlib
import random
from dataclasses import dataclass

from django.db.models import Q

from apps.matches.models import Match
from apps.teams.models import Team
from services.llm_prediction import TeamsContext, predict_with_llm


@dataclass
class PredictionOutput:
    score_a: int
    score_b: int
    confidence: float
    reasoning: str


def _recent_form_score(team: Team) -> float:
    recent_matches = Match.objects.filter(
        Q(team_a=team) | Q(team_b=team),
        status=Match.Status.COMPLETED,
        actual_score_a__isnull=False,
        actual_score_b__isnull=False,
    ).order_by("-kickoff_time")[:5]

    if not recent_matches:
        # Fall back to ranking-informed baseline when no recent data exists.
        return max(20.0, 100.0 - (team.fifa_rank * 0.7))

    points = 0
    for match in recent_matches:
        team_score = match.actual_score_a if match.team_a_id == team.id else match.actual_score_b
        opp_score = match.actual_score_b if match.team_a_id == team.id else match.actual_score_a
        if team_score > opp_score:
            points += 3
        elif team_score == opp_score:
            points += 1

    return (points / (len(recent_matches) * 3)) * 100.0


def _player_strength_simulation(team_a: Team, team_b: Team) -> tuple[float, float]:
    seed_key = f"{team_a.id}:{team_b.id}"
    seed = int(hashlib.sha256(seed_key.encode("utf-8")).hexdigest()[:8], 16)
    rng = random.Random(seed)

    base_a = max(45.0, 100.0 - (team_a.fifa_rank * 0.6))
    base_b = max(45.0, 100.0 - (team_b.fifa_rank * 0.6))

    variance_a = rng.uniform(-8.0, 8.0)
    variance_b = rng.uniform(-8.0, 8.0)

    return base_a + variance_a, base_b + variance_b


def generate_prediction(team_a: Team, team_b: Team) -> PredictionOutput:
    """Generate prediction using real LLM if available, else use heuristic engine."""
    # Try LLM first
    llm_result = _try_llm_prediction(team_a, team_b)
    if llm_result:
        return llm_result

    # Fall back to heuristic
    return _heuristic_prediction(team_a, team_b)


def _try_llm_prediction(team_a: Team, team_b: Team) -> PredictionOutput | None:
    """Attempt to use a real LLM for prediction."""
    try:
        recent_a = Match.objects.filter(
            Q(team_a=team_a) | Q(team_b=team_a),
            status=Match.Status.COMPLETED,
            actual_score_a__isnull=False,
        ).order_by("-kickoff_time")[:3]
        recent_b = Match.objects.filter(
            Q(team_a=team_b) | Q(team_b=team_b),
            status=Match.Status.COMPLETED,
            actual_score_a__isnull=False,
        ).order_by("-kickoff_time")[:3]

        results_a = ", ".join(
            f"{m.team_a.country_code if m.team_a_id == team_a.id else m.team_b.country_code} "
            f"{m.actual_score_a}-{m.actual_score_b}"
            for m in recent_a
        ) or "No recent matches"
        results_b = ", ".join(
            f"{m.team_a.country_code if m.team_a_id == team_b.id else m.team_b.country_code} "
            f"{m.actual_score_a}-{m.actual_score_b}"
            for m in recent_b
        ) or "No recent matches"

        context = TeamsContext(
            team_a_name=team_a.name,
            team_a_rank=team_a.fifa_rank,
            team_a_recent_results=results_a,
            team_b_name=team_b.name,
            team_b_rank=team_b.fifa_rank,
            team_b_recent_results=results_b,
            stage="World Cup",
        )

        llm_pred = predict_with_llm(context)
        if llm_pred:
            return PredictionOutput(
                score_a=llm_pred.score_a,
                score_b=llm_pred.score_b,
                confidence=llm_pred.confidence,
                reasoning=f"[{llm_pred.model}] {llm_pred.reasoning}",
            )
    except Exception as e:
        print(f"LLM prediction failed: {e}, falling back to heuristic")

    return None


def _heuristic_prediction(team_a: Team, team_b: Team) -> PredictionOutput:
    rank_a = max(0.0, 100.0 - team_a.fifa_rank)
    rank_b = max(0.0, 100.0 - team_b.fifa_rank)

    form_a = _recent_form_score(team_a)
    form_b = _recent_form_score(team_b)

    strength_a, strength_b = _player_strength_simulation(team_a, team_b)

    score_a_weighted = (rank_a * 0.30) + (form_a * 0.20) + (strength_a * 0.50)
    score_b_weighted = (rank_b * 0.30) + (form_b * 0.20) + (strength_b * 0.50)

    diff = score_a_weighted - score_b_weighted

    if diff > 12:
        score_a, score_b = 2, 0
    elif diff > 5:
        score_a, score_b = 2, 1
    elif diff < -12:
        score_a, score_b = 0, 2
    elif diff < -5:
        score_a, score_b = 1, 2
    else:
        score_a, score_b = 1, 1

    confidence = min(95.0, max(50.0, 60.0 + (abs(diff) * 0.9)))
    stronger_side = team_a.name if diff >= 0 else team_b.name

    reasoning = (
        f"[Heuristic Engine] {stronger_side} has better weighted indicators: FIFA ranking (30%), "
        f"recent form (20%), and player strength simulation (50%)."
    )

    return PredictionOutput(
        score_a=score_a,
        score_b=score_b,
        confidence=round(confidence, 2),
        reasoning=reasoning,
    )
