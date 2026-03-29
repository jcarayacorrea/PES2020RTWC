import random
from typing import List, Dict, Any, Optional
from fixtures import get_zone_data


def shuffle_and_pick(teams: List[Any], pick_size: int) -> List[Any]:
    """Shuffles a list and returns a slice of the given size."""
    shuffled_teams = teams.copy()
    random.shuffle(shuffled_teams)
    return shuffled_teams[:pick_size]


def round_draw(teams: List[Any], pools_count: int = 5, teams_per_pool: int = 2) -> List[List[Any]]:
    """Draws teams into different zones from sorted pools."""
    zones: List[List[Any]] = [[] for _ in range(teams_per_pool)]
    for p in range(pools_count):
        pool = shuffle_and_pick(teams[p * teams_per_pool:(p + 1) * teams_per_pool], teams_per_pool)
        for idx, team in enumerate(pool):
            zones[idx].append(team)
    return zones


def get_zone_with_teams_of_size(zone_code: str, conf_name: str, round_name: str, team_size: int = 4) -> Optional[List[Dict[str, Any]]]:
    """Retrieves teams from a zone only if it matches the expected size."""
    zone_data = get_zone_data(zone_code, conf_name, round_name)
    if len(zone_data['teams']) == team_size:
        return zone_data['teams']
    return None