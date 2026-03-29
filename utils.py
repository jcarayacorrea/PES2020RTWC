from typing import Any, Dict, List, Optional
from pymongo import MongoClient
from pymongo.database import Database
from django.conf import settings

def db_conexion() -> Database:
    """Establishes a connection to the MongoDB database."""
    client: MongoClient = MongoClient(host=settings.MONGO_URL,
                                     port=settings.MONGO_PORT,
                                     username=settings.MONGO_USERNAME,
                                     password=settings.MONGO_PASSWORD)
    return client[settings.MONGO_DBNAME]


def _get_teams(filter_query: Dict[str, Any], sort_field: str = 'fifa_nation_rank', sort_order: int = 1) -> List[Dict[str, Any]]:
    """Helper function to fetch and sort teams from the database."""
    db = db_conexion()
    cursor = db.get_collection('Teams').find(filter_query).sort(sort_field, sort_order)
    return list(cursor)


def get_teams(conf_name: str) -> List[Dict[str, Any]]:
    """Fetches all teams for a given confederation."""
    return _get_teams({'conf_name': conf_name})


def get_teams_first_round(conf_name: str) -> List[Dict[str, Any]]:
    """Fetches teams for the first round of a confederation."""
    return _get_teams({'conf_name': conf_name, 'stage.firstRound': True})


def get_teams_second_round(conf_name: str) -> List[Dict[str, Any]]:
    """Fetches teams for the second round of a confederation."""
    return _get_teams({'conf_name': conf_name, 'stage.secondRound': True})


def get_teams_third_round(conf_name: str) -> List[Dict[str, Any]]:
    """Fetches teams for the third round of a confederation."""
    return _get_teams({'conf_name': conf_name, 'stage.thirdRound': True})


def get_teams_final_round(conf_name: str) -> List[Dict[str, Any]]:
    """Fetches teams for the final round of a confederation."""
    return _get_teams({'conf_name': conf_name, 'stage.finalRound': True})


def get_teams_playoff() -> List[Dict[str, Any]]:
    """Fetches teams for the playoffs."""
    return _get_teams({'stage.playoff': True})


def get_uefa_teams_playoff(conf_name: str) -> List[Dict[str, Any]]:
    """Fetches UEFA teams for the playoffs."""
    return _get_teams({'conf_name': conf_name, 'stage.playoff': True})


def get_teams_main_draw() -> List[Dict[str, Any]]:
    """Fetches teams for the main draw."""
    return _get_teams({'stage.mainDraw': True})


def get_teams_copa_america() -> List[Dict[str, Any]]:
    """Fetches teams for Copa America (CONMEBOL + qualified CONCACAF)."""
    filter_condition = {
        '$or': [
            {'conf_name': 'CONMEBOL'},
            {
                '$and': [
                    {'conf_name': 'CONCACAF'},
                    {'$or': [{'stage.mainDraw': True}, {'stage.playoff': True}]}
                ]
            }
        ]
    }
    return _get_teams(filter_condition)


def generate_stage_obj(stage: str) -> Dict[str, bool]:
    """Generates a stage object with the active stage set to True."""
    stages = ['firstRound', 'secondRound', 'thirdRound', 'finalRound', 'playoff', 'mainDraw']
    return {stage_key: stage_key == stage for stage_key in stages}


def update_stage(iso_code: str, stage: str) -> None:
    """Updates the stage of a team in the database."""
    db = db_conexion()
    stage_obj = generate_stage_obj(stage)
    id_obj = {'nation_iso_code': iso_code}
    db.get_collection('Teams').update_one(id_obj, {'$set': {'stage': stage_obj}})


def get_teams_json() -> List[Dict[str, Any]]:
    """Fetches all teams without their MongoDB internal ID."""
    return _get_teams({}, sort_field='fifa_nation_rank')


def get_qualy_places(conf: str) -> List[Dict[str, Any]]:
    """Fetches qualification places for a confederation."""
    db = db_conexion()
    cursor = db.get_collection('Places').find({"conf": conf})
    return list(cursor)


def get_stage_data(stage: str, places: Dict[str, Any]) -> List[Any]:
    """Extracts stage data from the places dictionary."""
    places_dict = places.get('places', {})
    mapping = {
        'first': 'firstRound',
        'second': 'secondRound',
        'third': 'thirdRound',
        'final': 'finalRound'
    }
    stage_key = mapping.get(stage)
    return places_dict.get(stage_key, []) if stage_key else []


def get_round_stages(places_list: List[Dict[str, Any]], stage: str) -> List[Any]:
    """Fetches stages for a specific round."""
    if not places_list:
        return []
    return get_stage_data(stage, places_list[0])


def get_team_by_id(iso_code: str) -> List[Dict[str, Any]]:
    """Fetches a team by its ISO code."""
    db = db_conexion()
    return list(db.get_collection('Teams').find({'nation_iso_code': iso_code}))


def update_one_match_result_db(conf: str, round_name: str, zone: str, spec: Dict[str, Any]) -> None:
    """Updates a single match result in the database."""
    db = db_conexion()
    db.get_collection('Fixtures').update_many(
        {'conf': conf, 'round': round_name, 'zone': zone}, {'$set': spec})


def save_match_result(fixture_num: int, match_num: int, local_goals: int, away_goals: int, conf: str, round_name: str, zone: str) -> None:
    """Saves a match result to the database."""
    db = db_conexion()
    match_path = f'fixtures.fixture{fixture_num}.match{match_num}'

    db.get_collection('Fixtures').update_many(
        {'conf': conf, 'round': round_name, 'zone': zone},
        {'$set': {
            f'{match_path}.homeTeam.goals': local_goals,
            f'{match_path}.awayTeam.goals': away_goals,
            f'{match_path}.homeTeam.result': local_goals > away_goals,
            f'{match_path}.awayTeam.result': local_goals < away_goals,
            f'{match_path}.played': True
        }}
    )


def create_match_spec(phase: str, match_num: int, local_goals: int, away_goals: int, local_penalties: Optional[int], away_penalties: Optional[int]) -> Dict[str, Any]:
    """Creates a specification object for updating a match with goals and penalties."""
    return {
        f'fixtures.{phase}.match{match_num}.homeTeam.goals': local_goals,
        f'fixtures.{phase}.match{match_num}.awayTeam.goals': away_goals,
        f'fixtures.{phase}.match{match_num}.homeTeam.penalties': local_penalties,
        f'fixtures.{phase}.match{match_num}.awayTeam.penalties': away_penalties,
        f'fixtures.{phase}.match{match_num}.homeTeam.result': local_goals > away_goals or (
                local_goals == away_goals and local_penalties is not None and away_penalties is not None and local_penalties > away_penalties),
        f'fixtures.{phase}.match{match_num}.awayTeam.result': local_goals < away_goals or (
                local_goals == away_goals and local_penalties is not None and away_penalties is not None and local_penalties < away_penalties),
        f'fixtures.{phase}.match{match_num}.played': True
    }


def move_winner_spec(phase: str, match_num: int, team: Dict[str, Any]) -> Dict[str, Any]:
    """Creates a specification object to move a winner to the next phase."""
    return {
        f'fixtures.{phase}.match{match_num}.awayTeam.team': team
    }


def save_extra_time_result(phase: str, match: int, local_goals: int, away_goals: int, local_penalties: int, away_penalties: int, conf: str, round_name: str, zone: str, home_id: str, away_id: str) -> None:
    """Saves an extra time match result, including penalties if necessary."""
    final_match_spec = create_match_spec(phase, match, local_goals, away_goals, local_penalties, away_penalties)
    update_one_match_result_db(conf, round_name, zone, final_match_spec)
    
    if round_name == 'playoff' and phase == 'first':
        is_home_winner = local_goals > away_goals or (local_goals == away_goals and local_penalties > away_penalties)
        winner_id = home_id if is_home_winner else away_id
        winner_team = move_winner_spec('final', match, get_team_by_id(winner_id)[0])
        update_one_match_result_db(conf, round_name, zone, winner_team)


def is_difference_in_range(local_score: int, visitor_score: int, range_start: int, range_end: float) -> bool:
    """Checks if the difference between two scores is within a given range."""
    difference = abs(local_score - visitor_score)
    return range_start <= difference < range_end


def medium_difference(local_score: int, visitor_score: int) -> bool:
    return is_difference_in_range(local_score, visitor_score, 10, 20)


def high_difference(local_score: int, visitor_score: int) -> bool:
    return is_difference_in_range(local_score, visitor_score, 20, 30)


def extreme_difference(local_score: int, visitor_score: int) -> bool:
    return is_difference_in_range(local_score, visitor_score, 30, 70)


def ultra_difference(local_score: int, visitor_score: int) -> bool:
    return is_difference_in_range(local_score, visitor_score, 70, float('inf'))


def filter_team(conf: str, text_like: str) -> List[Dict[str, Any]]:
    """Filters teams by confederation and name using regex."""
    db = db_conexion()
    return list(db.get_collection('Teams').find(
        {'conf_name': conf, 'nation_name': {'$regex': text_like, '$options': 'is'}}))
