from html import escape

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.scoreboard.serializers import ScoreboardSerializer
from apps.scoreboard.services import recalculate_scoreboard


class ScoreboardView(APIView):
    def get(self, request):
        scoreboard = recalculate_scoreboard()
        return Response(ScoreboardSerializer(scoreboard).data)


class ScoreboardSocialCardView(APIView):
    def get(self, request):
        scoreboard = recalculate_scoreboard()
        ratio = request.query_params.get("ratio", "9:16")
        if ratio == "16:9":
            width, height = 1600, 900
        elif ratio == "1:1":
            width, height = 1080, 1080
        else:
            width, height = 1080, 1920

        if scoreboard.human_points == scoreboard.ai_points:
            leader = "TIE"
        elif scoreboard.human_points > scoreboard.ai_points:
            leader = "HUMAN LEADS"
        else:
            leader = "AI LEADS"

        svg = f"""
<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>
    <defs>
        <linearGradient id='bg' x1='0%' y1='0%' x2='100%' y2='100%'>
            <stop offset='0%' stop-color='#050505'/>
            <stop offset='100%' stop-color='#121314'/>
        </linearGradient>
        <radialGradient id='aiglow' cx='20%' cy='15%' r='45%'>
            <stop offset='0%' stop-color='rgba(0,219,233,0.35)'/>
            <stop offset='100%' stop-color='rgba(0,219,233,0)'/>
        </radialGradient>
        <radialGradient id='humanglow' cx='80%' cy='85%' r='45%'>
            <stop offset='0%' stop-color='rgba(169,249,0,0.28)'/>
            <stop offset='100%' stop-color='rgba(169,249,0,0)'/>
        </radialGradient>
    </defs>

    <rect width='100%' height='100%' fill='url(#bg)' />
    <rect width='100%' height='100%' fill='url(#aiglow)' />
    <rect width='100%' height='100%' fill='url(#humanglow)' />

    <rect x='{int(width * 0.06)}' y='{int(height * 0.06)}' width='{int(width * 0.88)}' height='{int(height * 0.88)}' rx='38' fill='rgba(255,255,255,0.04)' stroke='rgba(255,255,255,0.12)' />

    <text x='{int(width * 0.1)}' y='{int(height * 0.16)}' fill='#7df4ff' font-size='{int(width * 0.036)}' font-family='JetBrains Mono, monospace' letter-spacing='2'>AI vs ME</text>
    <text x='{int(width * 0.1)}' y='{int(height * 0.22)}' fill='#e5e2e3' font-size='{int(width * 0.07)}' font-family='Archivo Narrow, sans-serif' font-weight='700'>WORLD CUP PREDICTOR</text>
    <text x='{int(width * 0.1)}' y='{int(height * 0.30)}' fill='#b9cacb' font-size='{int(width * 0.042)}' font-family='Inter, sans-serif'>{escape(leader)}</text>

    <text x='{int(width * 0.14)}' y='{int(height * 0.50)}' fill='#a9f900' font-size='{int(width * 0.032)}' font-family='JetBrains Mono, monospace'>HUMAN</text>
    <text x='{int(width * 0.14)}' y='{int(height * 0.62)}' fill='#a9f900' font-size='{int(width * 0.16)}' font-family='Archivo Narrow, sans-serif' font-weight='700'>{scoreboard.human_points}</text>

    <text x='{int(width * 0.78)}' y='{int(height * 0.50)}' fill='#7df4ff' font-size='{int(width * 0.032)}' text-anchor='end' font-family='JetBrains Mono, monospace'>AI</text>
    <text x='{int(width * 0.78)}' y='{int(height * 0.62)}' fill='#7df4ff' font-size='{int(width * 0.16)}' text-anchor='end' font-family='Archivo Narrow, sans-serif' font-weight='700'>{scoreboard.ai_points}</text>

    <text x='{int(width * 0.50)}' y='{int(height * 0.58)}' fill='rgba(255,255,255,0.45)' text-anchor='middle' font-size='{int(width * 0.06)}' font-family='Archivo Narrow, sans-serif' font-weight='700'>VS</text>

    <text x='{int(width * 0.10)}' y='{int(height * 0.76)}' fill='#b9cacb' font-size='{int(width * 0.03)}' font-family='Inter, sans-serif'>Exact Hits: Human {scoreboard.human_exact_scores} | AI {scoreboard.ai_exact_scores}</text>
    <text x='{int(width * 0.10)}' y='{int(height * 0.81)}' fill='#b9cacb' font-size='{int(width * 0.03)}' font-family='Inter, sans-serif'>Matches Graded: {scoreboard.total_matches}</text>
    <text x='{int(width * 0.10)}' y='{int(height * 0.90)}' fill='rgba(255,255,255,0.70)' font-size='{int(width * 0.032)}' font-family='JetBrains Mono, monospace'>Share your score war: #AIvsMeWorldCup</text>
</svg>
""".strip()

        response = HttpResponse(svg, content_type="image/svg+xml")
        response["Cache-Control"] = "no-store"
        return response
