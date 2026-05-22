from typing import Any, Dict, List, Optional
from db import db_conexion


def update_one_match_result_db(conf: str, round_name: str, zone: str, spec: Dict[str, Any]) -> None:
    """Updates a single match result in the database."""
    db = db_conexion()
    db.get_collection('Fixtures').update_many(
        {'conf': conf, 'round': round_name, 'zone': zone}, {'$set': spec})


def save_match_result(fixture_num: Any, match_num: int, local_goals: int, away_goals: int, conf: str, round_name: str, zone: str) -> None:
    """Saves a match result to the database."""
    db = db_conexion()
    match_path = f"fixtures.fixture{fixture_num}.match{match_num}" if str(fixture_num).isdigit() else f"fixtures.{fixture_num}.match{match_num}"

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


def create_match_spec(phase: Any, match_num: int, local_goals: int, away_goals: int, local_penalties: Optional[int], away_penalties: Optional[int]) -> Dict[str, Any]:
    """Creates a specification object for updating a match with goals and penalties."""
    match_path = f"fixtures.fixture{phase}.match{match_num}" if str(phase).isdigit() else f"fixtures.{phase}.match{match_num}"
    return {
        f'{match_path}.homeTeam.goals': local_goals,
        f'{match_path}.awayTeam.goals': away_goals,
        f'{match_path}.homeTeam.penalties': local_penalties,
        f'{match_path}.awayTeam.penalties': away_penalties,
        f'{match_path}.homeTeam.result': local_goals > away_goals or (
                local_goals == away_goals and local_penalties is not None and away_penalties is not None and local_penalties > away_penalties),
        f'{match_path}.awayTeam.result': local_goals < away_goals or (
                local_goals == away_goals and local_penalties is not None and away_penalties is not None and local_penalties < away_penalties),
        f'{match_path}.played': True
    }


def move_winner_spec(phase: str, match_num: int, team: Dict[str, Any]) -> Dict[str, Any]:
    """Creates a specification object to move a winner to the next phase."""
    return {
        f'fixtures.{phase}.match{match_num}.awayTeam.team': team
    }


def save_extra_time_result(phase: Any, match: int, local_goals: int, away_goals: int, local_penalties: int, away_penalties: int, conf: str, round_name: str, zone: str, home_id: str, away_id: str) -> None:
    """Saves an extra time match result, including penalties if necessary."""
    final_match_spec = create_match_spec(phase, match, local_goals, away_goals, local_penalties, away_penalties)
    update_one_match_result_db(conf, round_name, zone, final_match_spec)

    if round_name == 'playoff' and phase == 'first':
        is_home_winner = local_goals > away_goals or (local_goals == away_goals and local_penalties > away_penalties)
        winner_id = home_id if is_home_winner else away_id
        from repositories.teams import get_team_by_id
        winner_team = move_winner_spec('final', match, get_team_by_id(winner_id)[0])
        update_one_match_result_db(conf, round_name, zone, winner_team)


def update_stage(iso_code: str, stage: str) -> None:
    """Updates the stage of a team in the database."""
    db = db_conexion()
    stage_obj = generate_stage_obj(stage)
    id_obj = {'nation_iso_code': iso_code}
    db.get_collection('Teams').update_one(id_obj, {'$set': {'stage': stage_obj}})


def generate_stage_obj(stage: str) -> Dict[str, bool]:
    """Generates a stage object with the active stage set to True."""
    stages = ['firstRound', 'secondRound', 'thirdRound', 'finalRound', 'playoff', 'mainDraw']
    return {stage_key: stage_key == stage for stage_key in stages}
