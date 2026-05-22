"""Backward-compatibility re-exports for the refactored module structure.

All functions previously defined here now live in focused modules:
  - db.py          — MongoDB connection management
  - repositories/  — teams, fixtures, places data access
"""

from db import db_conexion
from repositories.teams import (
    get_teams, get_teams_first_round, get_teams_second_round,
    get_teams_third_round, get_teams_final_round, get_teams_playoff,
    get_uefa_teams_playoff, get_teams_main_draw, get_teams_copa_america,
    get_teams_json, get_team_by_id, filter_team,
)
from repositories.fixtures import (
    save_match_result, save_extra_time_result, update_stage,
    generate_stage_obj, update_one_match_result_db,
    create_match_spec, move_winner_spec,
)
from repositories.places import (
    get_qualy_places, get_round_stages, get_stage_data,
)


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
