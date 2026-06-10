import os
from dataclasses import dataclass

# LLM_PROVIDER can be 'anthropic', 'openai', or 'heuristic'
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "heuristic")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


@dataclass
class TeamsContext:
    team_a_name: str
    team_a_rank: int
    team_a_recent_results: str
    team_b_name: str
    team_b_rank: int
    team_b_recent_results: str
    stage: str


@dataclass
class MatchPrediction:
    score_a: int
    score_b: int
    confidence: float
    reasoning: str
    model: str


def _format_prompt(context: TeamsContext) -> str:
    """Format a prompt for the LLM to predict match outcome."""
    return f"""You are a world-class football analytics AI. Predict the outcome of this World Cup match.

Match: {context.team_a_name} vs {context.team_b_name}
Stage: {context.stage}

Team A ({context.team_a_name}):
- FIFA Rank: {context.team_a_rank}
- Recent Results: {context.team_a_recent_results}

Team B ({context.team_b_name}):
- FIFA Rank: {context.team_b_rank}
- Recent Results: {context.team_b_recent_results}

Respond in JSON format with these exact fields:
{{
  "score_a": <int 0-3>,
  "score_b": <int 0-3>,
  "confidence": <float 50-95>,
  "reasoning": "<short sentence explaining your prediction>"
}}

Your reasoning should mention:
- Which team has the advantage
- Key tactical or form factors
- Expected style of play

Only respond with the JSON object, no markdown or extra text."""


def predict_with_llm(context: TeamsContext) -> MatchPrediction | None:
    """Call an LLM to generate prediction with reasoning."""
    if LLM_PROVIDER == "anthropic":
        return _predict_with_anthropic(context)
    elif LLM_PROVIDER == "openai":
        return _predict_with_openai(context)
    return None


def _predict_with_anthropic(context: TeamsContext) -> MatchPrediction | None:
    """Use Anthropic Claude API."""
    if not ANTHROPIC_API_KEY:
        return None

    try:
        import anthropic
    except ImportError:
        return None

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=256,
            messages=[{"role": "user", "content": _format_prompt(context)}],
        )

        response_text = message.content[0].text
        import json

        data = json.loads(response_text)
        return MatchPrediction(
            score_a=int(data.get("score_a", 1)),
            score_b=int(data.get("score_b", 1)),
            confidence=float(data.get("confidence", 65.0)),
            reasoning=data.get("reasoning", "AI analysis of team matchup"),
            model="Claude 3.5 Sonnet",
        )
    except Exception as e:
        print(f"Anthropic LLM error: {e}")
        return None


def _predict_with_openai(context: TeamsContext) -> MatchPrediction | None:
    """Use OpenAI GPT API."""
    if not OPENAI_API_KEY:
        return None

    try:
        import openai
    except ImportError:
        return None

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=256,
            messages=[{"role": "user", "content": _format_prompt(context)}],
        )

        response_text = response.choices[0].message.content
        import json

        data = json.loads(response_text)
        return MatchPrediction(
            score_a=int(data.get("score_a", 1)),
            score_b=int(data.get("score_b", 1)),
            confidence=float(data.get("confidence", 65.0)),
            reasoning=data.get("reasoning", "AI analysis based on team metrics"),
            model="GPT-4o Mini",
        )
    except Exception as e:
        print(f"OpenAI LLM error: {e}")
        return None
