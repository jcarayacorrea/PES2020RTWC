from typing import List, Dict, Any, Optional
from utils import db_conexion

def create_match(home_team: Dict[str, Any], away_team: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Creates a match dictionary object."""
    return {
        "homeTeam": {"team": home_team, "goals": None, "penalties": None, "result": False},
        "awayTeam": {"team": away_team, "goals": None, "penalties": None, "result": False},
        "played": False
    }


def create_fixture(teams: List[Dict[str, Any]], home_away_indicator: bool, zone: str, conf: str, round_name: str) -> None:
    """Generates a fixture schedule based on the number of teams."""
    matches_schedule: Dict[str, Any] = {}
    num_teams = len(teams)
    
    if num_teams == 3:
        schedule = [
            (0, 1, 2), (2, 0, 1), (1, 2, 0)
        ]
        if home_away_indicator:
            schedule += [(1, 0, 2), (0, 2, 1), (2, 1, 0)]
            
        for i, (h, a, b) in enumerate(schedule):
            matches_schedule[f"fixture{i+1}"] = {
                "match1": create_match(teams[h], teams[a]),
                "byeTeam": teams[b]
            }
            
    elif num_teams == 4:
        schedule = [
            ((0, 1), (2, 3)), ((3, 0), (1, 2)), ((1, 3), (0, 2))
        ]
        if home_away_indicator:
            schedule += [((1, 0), (3, 2)), ((0, 3), (2, 1)), ((3, 1), (2, 0))]
            
        for i, matches in enumerate(schedule):
            matches_schedule[f"fixture{i+1}"] = {
                "match1": create_match(teams[matches[0][0]], teams[matches[0][1]]),
                "match2": create_match(teams[matches[1][0]], teams[matches[1][1]]),
                "byeTeam": None
            }
            
    elif num_teams == 5:
        schedule = [
            ((0, 1), (2, 3), 4), ((4, 0), (1, 2), 3), ((1, 4), (3, 0), 2),
            ((3, 1), (2, 4), 0), ((0, 2), (4, 3), 1)
        ]
        if home_away_indicator:
            schedule += [
                ((1, 0), (3, 2), 4), ((0, 4), (2, 1), 3), ((4, 1), (0, 3), 2),
                ((1, 3), (4, 2), 0), ((2, 0), (3, 4), 1)
            ]
            
        for i, (m1, m2, b) in enumerate(schedule):
            matches_schedule[f"fixture{i+1}"] = {
                "match1": create_match(teams[m1[0]], teams[m1[1]]),
                "match2": create_match(teams[m2[0]], teams[m2[1]]),
                "byeTeam": teams[b]
            }

    update_fixture(teams, matches_schedule, zone, conf, round_name)


def update_fixture(teams: List[Dict[str, Any]], fixtures: Dict[str, Any], zone: str, conf: str, round_name: str) -> None:
    """Updates the fixture information in the database."""
    db = db_conexion()
    db.get_collection('Fixtures').update_one(
        {'conf': conf, 'zone': zone, 'round': round_name},
        {'$set': {'teams': teams, 'fixtures': fixtures}}
    )


def get_zone_data(zone: str, conf: str, round_name: str) -> Dict[str, Any]:
    """Retrieves fixture data for a specific zone, confederation, and round."""
    db = db_conexion()
    fixture = db.get_collection('Fixtures').find_one({'conf': conf, 'zone': zone, 'round': round_name})
    if not fixture:
        raise ValueError(f"Fixture not found for {conf} {zone} {round_name}")
    return fixture


def create_playoff_matches(teams: List[Dict[str, Any]], seeds: List[Dict[str, Any]], pool1: List[Dict[str, Any]], pool2: List[Dict[str, Any]]) -> None:
    """Creates playoff matches between pools and seeded teams."""
    match_structure: Dict[str, Any] = {"first": {}, "final": {}}
    for i in range(6):
        match_name = f"match{i + 1}"
        match_structure["first"][match_name] = create_match(pool1[i], pool2[i])
        match_structure["final"][match_name] = create_match(seeds[i], None)

    update_fixture(teams, match_structure, 'P', 'FIFA', 'playoff')


def create_playoff_matches_uefa(teams: List[Dict[str, Any]], pool1: List[Dict[str, Any]], pool2: List[Dict[str, Any]]) -> None:
    """Creates UEFA-specific playoff matches."""
    match_structure: Dict[str, Any] = {"euro": {}}
    for i in range(4):
        match_name = f"match{i + 1}"
        match_structure["euro"][match_name] = create_match(pool1[i], pool2[i])

    update_fixture(teams, match_structure, 'P', 'UEFA', 'playoff')
