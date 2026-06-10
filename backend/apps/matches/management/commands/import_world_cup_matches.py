from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from urllib.request import Request, urlopen

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.matches.models import Match
from apps.teams.models import Team

WORLDCUPJSON_URL = "https://worldcupjson.net/matches"
OPENFOOTBALL_2022_URL = "https://raw.githubusercontent.com/openfootball/world-cup.json/master/2022/worldcup.json"


@dataclass
class ImportMatch:
    team_a_name: str
    team_b_name: str
    kickoff_time: datetime
    stage: str
    status: str
    actual_score_a: int | None
    actual_score_b: int | None
    stadium: str


def _fetch_json(url: str) -> Any:
    request = Request(url, headers={"User-Agent": "AIvsMeWorldCup/1.0"})
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def _normalize_stage(value: str) -> str:
    cleaned = (value or "group").strip().lower().replace(" ", "_")
    mapping = {
        "group_stage": Match.Stage.GROUP,
        "group": Match.Stage.GROUP,
        "round_of_16": Match.Stage.ROUND_OF_16,
        "round_of_16s": Match.Stage.ROUND_OF_16,
        "quarter_finals": Match.Stage.QUARTERFINAL,
        "quarter-finals": Match.Stage.QUARTERFINAL,
        "quarterfinal": Match.Stage.QUARTERFINAL,
        "semi_finals": Match.Stage.SEMIFINAL,
        "semi-finals": Match.Stage.SEMIFINAL,
        "semifinal": Match.Stage.SEMIFINAL,
        "third_place": Match.Stage.THIRD_PLACE,
        "play_off_for_third_place": Match.Stage.THIRD_PLACE,
        "final": Match.Stage.FINAL,
    }
    return mapping.get(cleaned, Match.Stage.GROUP)


def _parse_worldcupjson(payload: list[dict[str, Any]]) -> list[ImportMatch]:
    parsed: list[ImportMatch] = []
    for item in payload:
        dt_raw = item.get("datetime")
        if not dt_raw:
            continue
        kickoff = datetime.fromisoformat(dt_raw.replace("Z", "+00:00"))
        home_team = item.get("home_team") or {}
        away_team = item.get("away_team") or {}

        home_goals = home_team.get("goals")
        away_goals = away_team.get("goals")

        status_value = (item.get("status") or "future").lower()
        if status_value in {"future", "scheduled"}:
            status = Match.Status.UPCOMING
        elif status_value in {"in_progress", "live"}:
            status = Match.Status.LIVE
        else:
            status = Match.Status.COMPLETED

        parsed.append(
            ImportMatch(
                team_a_name=item.get("home_team_country") or "Unknown",
                team_b_name=item.get("away_team_country") or "Unknown",
                kickoff_time=kickoff,
                stage=_normalize_stage(item.get("stage_name") or "group"),
                status=status,
                actual_score_a=home_goals if status == Match.Status.COMPLETED else None,
                actual_score_b=away_goals if status == Match.Status.COMPLETED else None,
                stadium=item.get("venue") or item.get("location") or "",
            )
        )
    return parsed


def _parse_openfootball(payload: dict[str, Any]) -> list[ImportMatch]:
    parsed: list[ImportMatch] = []
    for round_item in payload.get("rounds", []):
        stage = _normalize_stage(round_item.get("name", "group"))
        for match in round_item.get("matches", []):
            date_str = match.get("date")
            time_str = match.get("time") or "00:00"
            if not date_str:
                continue
            kickoff = datetime.fromisoformat(f"{date_str}T{time_str}:00+00:00")
            score = match.get("score") or {}
            ft = score.get("ft") or []
            completed = len(ft) == 2

            parsed.append(
                ImportMatch(
                    team_a_name=match.get("team1", {}).get("name", "Unknown"),
                    team_b_name=match.get("team2", {}).get("name", "Unknown"),
                    kickoff_time=kickoff,
                    stage=stage,
                    status=Match.Status.COMPLETED if completed else Match.Status.UPCOMING,
                    actual_score_a=ft[0] if completed else None,
                    actual_score_b=ft[1] if completed else None,
                    stadium=match.get("stadium") or match.get("city") or "",
                )
            )
    return parsed


def _country_code(name: str) -> str:
    alias = {
        "United States": "USA",
        "Korea Republic": "KOR",
        "IR Iran": "IRN",
        "Saudi Arabia": "SAU",
        "Costa Rica": "CRC",
        "Germany": "GER",
        "England": "ENG",
        "France": "FRA",
        "Brazil": "BRA",
        "Argentina": "ARG",
        "Netherlands": "NED",
        "Portugal": "POR",
        "Spain": "ESP",
        "Croatia": "CRO",
        "Belgium": "BEL",
        "Switzerland": "SUI",
        "Australia": "AUS",
        "Poland": "POL",
        "Morocco": "MAR",
        "Japan": "JPN",
        "Mexico": "MEX",
        "Canada": "CAN",
        "Qatar": "QAT",
        "Ecuador": "ECU",
        "Senegal": "SEN",
        "Denmark": "DEN",
        "Tunisia": "TUN",
        "Cameroon": "CMR",
        "Serbia": "SRB",
        "Ghana": "GHA",
        "Uruguay": "URU",
        "Wales": "WAL",
    }
    if name in alias:
        return alias[name]
    letters = "".join(ch for ch in name.upper() if ch.isalpha())
    return (letters[:3] or "UNK").ljust(3, "X")


class Command(BaseCommand):
    help = "Import real World Cup teams and matches from a public dataset"

    def add_arguments(self, parser):
        parser.add_argument(
            "--source",
            choices=["worldcupjson", "openfootball"],
            default="worldcupjson",
            help="Dataset source to import from",
        )
        parser.add_argument(
            "--update-existing",
            action="store_true",
            help="Update existing records when kickoff collisions match",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        source = options["source"]
        update_existing = options["update_existing"]

        if source == "worldcupjson":
            payload = _fetch_json(WORLDCUPJSON_URL)
            matches = _parse_worldcupjson(payload)
        else:
            payload = _fetch_json(OPENFOOTBALL_2022_URL)
            matches = _parse_openfootball(payload)

        if not matches:
            self.stdout.write(self.style.WARNING("No matches parsed from source."))
            return

        teams_cache: dict[str, Team] = {}
        teams_created = 0
        matches_created = 0
        matches_updated = 0

        for item in matches:
            for team_name in (item.team_a_name, item.team_b_name):
                code = _country_code(team_name)
                if code in teams_cache:
                    continue
                team, created = Team.objects.get_or_create(
                    country_code=code,
                    defaults={
                        "name": team_name,
                        "fifa_rank": 100,
                        "group": None,
                    },
                )
                if created:
                    teams_created += 1
                elif team.name != team_name:
                    team.name = team_name
                    team.save(update_fields=["name"])
                teams_cache[code] = team

            team_a = teams_cache[_country_code(item.team_a_name)]
            team_b = teams_cache[_country_code(item.team_b_name)]

            existing = Match.objects.filter(
                team_a=team_a,
                team_b=team_b,
                kickoff_time=item.kickoff_time,
            ).first()

            if existing is None:
                Match.objects.create(
                    team_a=team_a,
                    team_b=team_b,
                    kickoff_time=item.kickoff_time,
                    stadium=item.stadium,
                    stage=item.stage,
                    actual_score_a=item.actual_score_a,
                    actual_score_b=item.actual_score_b,
                    status=item.status,
                )
                matches_created += 1
            elif update_existing:
                existing.stadium = item.stadium
                existing.stage = item.stage
                existing.actual_score_a = item.actual_score_a
                existing.actual_score_b = item.actual_score_b
                existing.status = item.status
                existing.save(
                    update_fields=[
                        "stadium",
                        "stage",
                        "actual_score_a",
                        "actual_score_b",
                        "status",
                    ]
                )
                matches_updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                (
                    f"Imported {len(matches)} matches from {source}. "
                    f"Teams created: {teams_created}. "
                    f"Matches created: {matches_created}. "
                    f"Matches updated: {matches_updated}."
                )
            )
        )
        self.stdout.write(f"Import completed at {timezone.now().isoformat()}")
