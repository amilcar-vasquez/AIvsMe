# AI vs Me: World Cup Predictor Backend

## Stack
- Django 5+
- Django REST Framework
- SQLite (default dev), PostgreSQL (optional via env vars)

## Quick Start
1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. `python manage.py makemigrations`
4. `python manage.py migrate`
5. `python manage.py runserver`

## API Endpoints
- `GET /api/teams/`
- `GET /api/teams/{id}/`
- `GET /api/matches/`
- `GET /api/matches/upcoming/`
- `GET /api/matches/completed/`
- `POST /api/matches/{id}/set-result/`
- `GET /api/predictions/`
- `POST /api/predictions/`
- `GET /api/matches/{id}/predictions/`
- `GET /api/scoreboard/`

## AI Engine

The prediction engine now uses **real Large Language Models** for authentic reasoning when predicting match outcomes.

### How It Works
1. **LLM First**: Calls Claude (Anthropic) or GPT (OpenAI) with team stats context
2. **Smart Fallback**: If LLM API fails or is disabled, uses deterministic heuristic
3. **Reasoning Tag**: UI displays which engine was used: `[Claude 3.5 Sonnet]` or `[Heuristic Engine]`

### Supported Providers

**Anthropic Claude** (Recommended)
```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
- Model: Claude 3.5 Sonnet
- ~$0.01-0.05 per prediction
- [Get API Key →](https://console.anthropic.com/)

**OpenAI GPT**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
- Model: GPT-4o mini  
- ~$0.001-0.005 per prediction
- [Get API Key →](https://platform.openai.com/api-keys)

**Heuristic Only** (No API)
```env
LLM_PROVIDER=heuristic
```
- Uses weighted scoring: FIFA ranking (30%), recent form (20%), player sim (50%)
- Zero cost, <100ms response time

### Example LLM Output
> [Claude 3.5 Sonnet] France demonstrates superior overall strength with FIFA ranking #4 vs #6, combined with recent tournament form advantage. Predicting 2-1 France victory based on attacking prowess and defensive solidity.

**Performance Metrics**
| Provider | Latency | Cost | Realism |
|----------|---------|------|---------|
| Claude | 3-5s | $0.02 | ⭐⭐⭐⭐⭐ |
| OpenAI | 2-4s | $0.003 | ⭐⭐⭐⭐ |
| Heuristic | <100ms | $0 | ⭐⭐⭐ |

### Setup

1. **Create `.env` file:**
   ```bash
   cp .env.example .env
   # Edit with your API key choice
   ```

2. **Install LLM libraries:**
   ```bash
   pip install -r requirements.txt
   ```
   (`anthropic` and `openai` packages included)

3. **Start server:**
   ```bash
   python manage.py runserver
   ```
   LLM calls are transparent to the API—just works!

### Fallback Behavior
If LLM API is unreachable, the system gracefully falls back to the heuristic engine:
```python
# ai_prediction_engine.py flow:
llm_result = _try_llm_prediction(team_a, team_b)  # Tries Claude/GPT
if llm_result:
    return llm_result  # ✅ LLM succeeded
else:
    return _heuristic_prediction(team_a, team_b)  # ⚠️ LLM failed, use heuristic
```

### Legacy Heuristic
`services/ai_prediction_engine.py` heuristic component uses:
- FIFA ranking: 30%
- Recent form: 20%
- Player strength simulation: 50%

## Real-World Data Import
Import public World Cup matches directly into `Team` and `Match` models:

- `python manage.py import_world_cup_matches --source worldcupjson --update-existing`
- `python manage.py import_world_cup_matches --source openfootball --update-existing`

Primary source:
- `https://worldcupjson.net/matches`

Fallback source:
- `https://raw.githubusercontent.com/openfootball/world-cup.json/master/2022/worldcup.json`
