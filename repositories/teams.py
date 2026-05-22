from typing import Any, Dict, List
from db import db_conexion


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


def get_teams_json() -> List[Dict[str, Any]]:
    """Fetches all teams without their MongoDB internal ID."""
    return _get_teams({}, sort_field='fifa_nation_rank')


def get_team_by_id(iso_code: str) -> List[Dict[str, Any]]:
    """Fetches a team by its ISO code."""
    db = db_conexion()
    return list(db.get_collection('Teams').find({'nation_iso_code': iso_code}))


def filter_team(conf: str, text_like: str) -> List[Dict[str, Any]]:
    """Filters teams by confederation and name using regex."""
    db = db_conexion()
    return list(db.get_collection('Teams').find(
        {'conf_name': conf, 'nation_name': {'$regex': text_like, '$options': 'is'}}))
