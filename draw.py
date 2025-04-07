import random
from fixtures import getZoneData


def shuffle_and_pick(teams, pick_size):
    random.shuffle(teams)
    return [teams[i] for i in range(pick_size)]


def round_draw(teams, pools_count=5, teams_per_pool=2):
    zones = [[] for _ in range(teams_per_pool)]
    for p in range(pools_count):
        pool = shuffle_and_pick(teams[p * teams_per_pool:(p + 1) * teams_per_pool], teams_per_pool)
        for idx, team in enumerate(pool):
            zones[idx].append(team)
    return zones

def get_zone_with_teams_of_size(zone_code, conf_name, round_name, team_size=4):
    zone_data = getZoneData(zone_code, conf_name, round_name)
    if len(zone_data['teams']) == team_size:
        return zone_data['teams']
    return None