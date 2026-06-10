from __future__ import annotations

import json
import zlib
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.matches.models import Match
from apps.teams.models import Team


@dataclass
class Fixture:
    match_number: int
    date: date
    stage: str
    team_a: str
    team_b: str
    stadium: str


TEAM_CODE_MAP = {
    "Algeria": "ALG",
    "Argentina": "ARG",
    "Australia": "AUS",
    "Austria": "AUT",
    "Belgium": "BEL",
    "Bosnia and Herzegovina": "BIH",
    "Brazil": "BRA",
    "Cabo Verde": "CPV",
    "Canada": "CAN",
    "Colombia": "COL",
    "Congo DR": "COD",
    "Cote d'Ivoire": "CIV",
    "Croatia": "CRO",
    "Curacao": "CUW",
    "Czechia": "CZE",
    "Ecuador": "ECU",
    "Egypt": "EGY",
    "England": "ENG",
    "France": "FRA",
    "Germany": "GER",
    "Ghana": "GHA",
    "Haiti": "HAI",
    "IR Iran": "IRN",
    "Iraq": "IRQ",
    "Japan": "JPN",
    "Jordan": "JOR",
    "Korea Republic": "KOR",
    "Mexico": "MEX",
    "Morocco": "MAR",
    "Netherlands": "NED",
    "New Zealand": "NZL",
    "Norway": "NOR",
    "Panama": "PAN",
    "Paraguay": "PAR",
    "Portugal": "POR",
    "Qatar": "QAT",
    "Saudi Arabia": "KSA",
    "Scotland": "SCO",
    "Senegal": "SEN",
    "South Africa": "RSA",
    "Spain": "ESP",
    "Sweden": "SWE",
    "Switzerland": "SUI",
    "Tunisia": "TUN",
    "Turkey": "TUR",
    "Uruguay": "URU",
    "USA": "USA",
    "Uzbekistan": "UZB",
}


def _load_fixtures() -> list[Fixture]:
    schedule_path = Path(__file__).resolve().parents[2] / "data" / "world_cup_2026_schedule.json"
    payload = json.loads(schedule_path.read_text(encoding="utf-8"))
    fixtures: list[Fixture] = []
    for row in payload:
        fixtures.append(
            Fixture(
                match_number=int(row["match_number"]),
                date=date.fromisoformat(row["date"]),
                stage=row["stage"],
                team_a=row["team_a"],
                team_b=row["team_b"],
                stadium=row["stadium"],
            )
        )
    return fixtures


def _stable_code(name: str, used_codes: set[str]) -> str:
    explicit = TEAM_CODE_MAP.get(name)
    if explicit and explicit not in used_codes:
        return explicit

    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    value = zlib.crc32(name.encode("utf-8")) % (36**3)
    while True:
        n = value
        chars = []
        for _ in range(3):
            n, remainder = divmod(n, 36)
            chars.append(alphabet[remainder])
        code = "".join(reversed(chars))
        if code not in used_codes:
            return code
        value = (value + 1) % (36**3)


def _normalize_stage(value: str) -> str:
    mapping = {
        "group": Match.Stage.GROUP,
        "round_of_32": "round_of_32",
        "round_of_16": Match.Stage.ROUND_OF_16,
        "quarterfinal": Match.Stage.QUARTERFINAL,
        "semifinal": Match.Stage.SEMIFINAL,
        "third_place": Match.Stage.THIRD_PLACE,
        "final": Match.Stage.FINAL,
    }
    return mapping.get(value, Match.Stage.GROUP)


class Command(BaseCommand):
    help = "Import FIFA World Cup 2026 schedule (104 matches) from local dataset"

    def add_arguments(self, parser):
        parser.add_argument(
            "--replace-existing",
            action="store_true",
            help="Delete existing future/upcoming matches in the 2026 tournament window before import",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        fixtures = _load_fixtures()
        if len(fixtures) != 104:
            self.stdout.write(self.style.ERROR(f"Expected 104 fixtures, got {len(fixtures)}."))
            return

        if options["replace_existing"]:
            deleted, _ = Match.objects.filter(
                kickoff_time__gte=datetime(2026, 6, 1, tzinfo=timezone.utc),
                kickoff_time__lt=datetime(2026, 8, 1, tzinfo=timezone.utc),
            ).delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted} existing match rows in 2026 window."))

        used_codes = set(Team.objects.values_list("country_code", flat=True))
        teams_cache: dict[str, Team] = {}
        created_teams = 0
        created_matches = 0

        matches_per_day: dict[date, int] = {}

        for fixture in fixtures:
            for team_name in (fixture.team_a, fixture.team_b):
                if team_name in teams_cache:
                    continue

                existing = Team.objects.filter(name=team_name).first()
                if existing:
                    teams_cache[team_name] = existing
                    used_codes.add(existing.country_code)
                    continue

                code = _stable_code(team_name, used_codes)
                used_codes.add(code)
                team = Team.objects.create(
                    name=team_name,
                    country_code=code,
                    fifa_rank=100,
                    group=None,
                )
                teams_cache[team_name] = team
                created_teams += 1

            slot = matches_per_day.get(fixture.date, 0)
            matches_per_day[fixture.date] = slot + 1

            kickoff_time = datetime.combine(
                fixture.date,
                time(hour=16, minute=0),
                tzinfo=timezone.utc,
            ) + timedelta(hours=slot * 3)

            _, created = Match.objects.get_or_create(
                team_a=teams_cache[fixture.team_a],
                team_b=teams_cache[fixture.team_b],
                kickoff_time=kickoff_time,
                defaults={
                    "stadium": fixture.stadium,
                    "stage": _normalize_stage(fixture.stage),
                    "status": Match.Status.UPCOMING,
                },
            )
            if created:
                created_matches += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported World Cup 2026 schedule: {created_teams} teams created, {created_matches} matches created."
            )
        )
