import random
from typing import List, Dict, Any
from repositories.teams import (
    get_teams, get_teams_first_round,
    get_teams_second_round, get_teams_third_round,
    get_teams_final_round, filter_team,
)
from repositories.fixtures import update_stage
from draw import round_draw, get_zone_with_teams_of_size
from fixtures import create_fixture, get_zone_data

from .models import Team

_ROUND_MAPPING = {
    'first': get_teams_first_round,
    'second': get_teams_second_round,
    'third': get_teams_third_round,
    'final': get_teams_final_round,
}


class ConfederationService:
    def __init__(self, conf_name: str):
        self.conf_name = conf_name

    def get_all_teams(self) -> List[Team]:
        return [Team(t) for t in get_teams(conf_name=self.conf_name)]

    def _get_round_teams_raw(self, round_type: str) -> List[Dict[str, Any]]:
        func = _ROUND_MAPPING.get(round_type)
        if not func:
            raise ValueError(f"Invalid round type: {round_type}")
        return func(conf_name=self.conf_name)

    def get_round_teams(self, round_type: str) -> List[Team]:
        return [Team(t) for t in self._get_round_teams_raw(round_type)]

    def get_round_context(self, round_name: str, zone_keys: List[str], team_size: int, group_range: Any) -> Dict[str, Any]:
        context = {
            'teams': self.get_round_teams(round_name),
            'range': group_range
        }
        for zone_code in zone_keys:
            teams = get_zone_with_teams_of_size(zone_code, self.conf_name, round_name, team_size=team_size)
            if teams is not None:
                context[f'zone{zone_code}'] = [Team(t) for t in teams]
        return context

    def perform_draw(self, round_name: str, pools_count: int, teams_per_pool: int, home_away: bool = True):
        raw_teams = self._get_round_teams_raw(round_name)
        zones = round_draw(raw_teams, pools_count=pools_count, teams_per_pool=teams_per_pool)
        for zone_idx, zone in enumerate(zones):
            random.shuffle(zone)
            zone_code = chr(ord('A') + zone_idx)
            create_fixture(zone, home_away, zone_code, self.conf_name, round_name)

    def update_team_progress(self, code: str, stage: str):
        update_stage(code, stage)

    def filter_teams(self, text: str) -> List[Dict[str, Any]]:
        return filter_team(self.conf_name, text)

    def set_final_team(self, zone: str, round_name: str, match_key: str, side: str, team_iso: str) -> None:
        """Sets a team as home or away in a final round match."""
        from repositories.teams import get_team_by_id
        from db import db_conexion
        team = get_team_by_id(team_iso)
        if not team:
            raise ValueError(f"Team {team_iso} not found")
        db = db_conexion()
        db.get_collection('Fixtures').update_many(
            {'conf': self.conf_name, 'zone': zone, 'round': round_name},
            {'$set': {
                f'fixtures.{match_key}.match1.{side}Team.team': team[0],
                f'fixtures.{match_key}.match1.{side}Team.goals': None,
                f'fixtures.{match_key}.match1.{side}Team.penalties': None,
                f'fixtures.{match_key}.match1.played': False
            }}
        )


_service_cache: Dict[str, ConfederationService] = {}


def get_service(conf_name: str) -> ConfederationService:
    """Returns a cached ConfederationService instance for the given confederation."""
    if conf_name not in _service_cache:
        _service_cache[conf_name] = ConfederationService(conf_name)
    return _service_cache[conf_name]
