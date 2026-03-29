import random
from typing import List, Dict, Any, Optional, Tuple
from utils import (
    get_teams, update_stage, get_teams_first_round,
    get_teams_second_round, get_teams_third_round,
    get_teams_final_round, filter_team
)
from draw import round_draw, get_zone_with_teams_of_size
from fixtures import create_fixture, get_zone_data

from .models import Team, Fixture

class ConfederationService:
    def __init__(self, conf_name: str):
        self.conf_name = conf_name

    def get_all_teams(self) -> List[Team]:
        return [Team(t) for t in get_teams(conf_name=self.conf_name)]

    def get_round_teams(self, round_type: str) -> List[Team]:
        mapping = {
            'first': get_teams_first_round,
            'second': get_teams_second_round,
            'third': get_teams_third_round,
            'final': get_teams_final_round
        }
        func = mapping.get(round_type)
        if not func:
            raise ValueError(f"Invalid round type: {round_type}")
        return [Team(t) for t in func(conf_name=self.conf_name)]

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
        teams_for_match = get_teams_final_round(conf_name=self.conf_name) # Fallback to final for generic draw if needed, but better use round-specific
        # Actually better use self.get_round_teams and extract raw data
        mapping = {
            'first': get_teams_first_round,
            'second': get_teams_second_round,
            'third': get_teams_third_round,
            'final': get_teams_final_round
        }
        raw_teams = mapping[round_name](conf_name=self.conf_name)
        zones = round_draw(raw_teams, pools_count=pools_count, teams_per_pool=teams_per_pool)
        for zone_idx, zone in enumerate(zones):
            random.shuffle(zone)
            zone_code = chr(ord('A') + zone_idx)
            create_fixture(zone, home_away, zone_code, self.conf_name, round_name)

    def update_team_progress(self, code: str, stage: str):
        update_stage(code, stage)

    def filter_teams(self, text: str) -> List[Dict[str, Any]]:
        return filter_team(self.conf_name, text)
