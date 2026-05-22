from typing import Any, Dict, List
from db import db_conexion


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
