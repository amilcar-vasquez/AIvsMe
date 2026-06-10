from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.matches.models import Match
from apps.teams.models import Team


TEAMS = [
    {"name": "Argentina", "country_code": "ARG", "fifa_rank": 1, "group": "C"},
    {"name": "France", "country_code": "FRA", "fifa_rank": 2, "group": "D"},
    {"name": "Brazil", "country_code": "BRA", "fifa_rank": 3, "group": "G"},
    {"name": "England", "country_code": "ENG", "fifa_rank": 4, "group": "B"},
    {"name": "Portugal", "country_code": "POR", "fifa_rank": 6, "group": "H"},
    {"name": "Netherlands", "country_code": "NED", "fifa_rank": 7, "group": "A"},
    {"name": "Croatia", "country_code": "CRO", "fifa_rank": 9, "group": "F"},
    {"name": "Germany", "country_code": "GER", "fifa_rank": 10, "group": "E"},
]

FIXTURES = [
    {"team_a": "BRA", "team_b": "FRA", "offset_hours": 24, "stadium": "Lusail", "stage": Match.Stage.QUARTERFINAL},
    {"team_a": "ARG", "team_b": "NED", "offset_hours": 30, "stadium": "Al Bayt", "stage": Match.Stage.QUARTERFINAL},
    {"team_a": "POR", "team_b": "ENG", "offset_hours": 48, "stadium": "Education City", "stage": Match.Stage.SEMIFINAL},
    {"team_a": "CRO", "team_b": "GER", "offset_hours": 54, "stadium": "974 Stadium", "stage": Match.Stage.SEMIFINAL},
]


class Command(BaseCommand):
    help = "Seed baseline World Cup teams and fixtures"

    def handle(self, *args, **options):
        teams_by_code = {}
        for payload in TEAMS:
            team, created = Team.objects.get_or_create(
                country_code=payload["country_code"],
                defaults=payload,
            )
            if not created:
                updated = False
                for key in ("name", "fifa_rank", "group"):
                    if getattr(team, key) != payload[key]:
                        setattr(team, key, payload[key])
                        updated = True
                if updated:
                    team.save(update_fields=["name", "fifa_rank", "group"])
            teams_by_code[team.country_code] = team

        now = timezone.now()
        created_matches = 0
        for fixture in FIXTURES:
            team_a = teams_by_code[fixture["team_a"]]
            team_b = teams_by_code[fixture["team_b"]]
            kickoff_time = now + timedelta(hours=fixture["offset_hours"])

            _, created = Match.objects.get_or_create(
                team_a=team_a,
                team_b=team_b,
                kickoff_time=kickoff_time,
                defaults={
                    "stadium": fixture["stadium"],
                    "stage": fixture["stage"],
                    "status": Match.Status.UPCOMING,
                },
            )
            if created:
                created_matches += 1

        self.stdout.write(self.style.SUCCESS(f"Seed complete: {len(TEAMS)} teams, {created_matches} new matches."))
