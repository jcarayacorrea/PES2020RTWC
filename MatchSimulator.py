import random
import time
from typing import Dict, List, Optional, Tuple, Any

from Global_Variables import (
    HOME_GOAL, AWAY_GOAL, GOAL_PRBLTY, STEP, SLEEP_TIME, GOAL, NO_GOAL, 
    PENALTY_DEFAULT_TURNS, LOG_LENGTH
)
from utils import (
    medium_difference, high_difference, extreme_difference, ultra_difference, 
    get_team_by_id
)


def calculate_probability(winner_rank: int, loser_rank: int) -> Tuple[float, float]:
    """Calculates the probability of the higher ranked team winning vs the lower ranked."""
    diff_functions = [medium_difference, high_difference, extreme_difference, ultra_difference]
    probabilities = [(0.65, 0.35), (0.7, 0.3), (0.8, 0.2), (0.9, 0.1)]

    for diff_func, probability in zip(diff_functions, probabilities):
        if diff_func(winner_rank, loser_rank):
            return probability
            
    # Default for small differences
    return (0.55, 0.45)


def calculate_winner_probability(home_rank: int, guest_rank: int) -> Tuple[float, float]:
    """Calculates home and guest win probabilities based on their FIFA ranks."""
    if home_rank < guest_rank:
        # Lower rank number is better in FIFA rankings
        return calculate_probability(home_rank, guest_rank)
    elif home_rank > guest_rank:
        # Guest team is better ranked
        guest_prob, home_prob = calculate_probability(guest_rank, home_rank)
        return home_prob, guest_prob
    else:
        # Equal ranks
        return 0.5, 0.5


def display_event(time_elapsed: int, name: str, home_goals: Optional[int], away_goals: Optional[int], 
                  penalties: List[str] = [], event_type: str = "Goal") -> None:
    """Prints match events to the console."""
    if event_type == 'Goal':
        print(f'GOAL {name} ({time_elapsed}") {home_goals} - {away_goals}\n')
    elif event_type == 'Penalties':
        print(f'PENALTY {name}  {"".join(penalties[-5:])}\n')
    elif event_type == 'Minute':
        print(f'Minute ({time_elapsed}")\n')


def process_match_event(event_time: int, home_prob: float, away_prob: float, 
                        home_name: str, away_name: str,
                        home_goals: int, away_goals: int) -> Tuple[int, int]:
    """Determines if a goal occurred during a specific match minute."""
    h_prob = home_prob * GOAL_PRBLTY
    a_prob = away_prob * GOAL_PRBLTY
    s_prob = 1 - (h_prob + a_prob)
    
    event = random.choices([HOME_GOAL, AWAY_GOAL, STEP], [h_prob, a_prob, s_prob])[0]
    
    if event == HOME_GOAL:
        home_goals += 1
        display_event(event_time, home_name, home_goals, away_goals)
    elif event == AWAY_GOAL:
        away_goals += 1
        display_event(event_time, away_name, home_goals, away_goals)
    else:
        display_event(event_time, home_name, home_goals, away_goals, event_type="Minute")
        
    return home_goals, away_goals


def simulate_match_time(start_time: int, duration: int, home_prob: float, away_prob: float, 
                        home_name: str, away_name: str, match_data: Dict[str, Any]) -> None:
    """Simulates match progression over a period of time."""
    for event_time in range(start_time, duration + 1):
        match_data['home_goals'], match_data['away_goals'] = process_match_event(
            event_time, home_prob, away_prob, home_name, away_name,
            match_data['home_goals'], match_data['away_goals']
        )
        time.sleep(SLEEP_TIME)


def execute_penalty(probability: float, name: str, penalty_array: List[str], current_penalties: int) -> int:
    """Simulates a single penalty kick."""
    event = random.choices([GOAL, NO_GOAL], [probability, 1 - probability])[0]
    penalty_array.append(event)
    if event == GOAL:
        current_penalties += 1
    display_event(0, name, None, None, penalty_array, event_type="Penalties")
    time.sleep(SLEEP_TIME)
    return current_penalties


def simulate_penalty_shots(home_prob: float, away_prob: float, home_name: str, away_name: str, 
                           match_data: Dict[str, Any]) -> None:
    """Simulates a penalty shootout until a winner is determined."""
    home_penalties_array: List[str] = []
    away_penalties_array: List[str] = []
    match_data['home_penalties'] = 0
    match_data['away_penalties'] = 0
    turns = 1
    penalty_kick_over = False
    
    print(f" PENALTIES {home_name} - {away_name} ".center(LOG_LENGTH, '='))

    while not penalty_kick_over:
        match_data['home_penalties'] = execute_penalty(
            home_prob, home_name, home_penalties_array, match_data['home_penalties']
        )
        match_data['away_penalties'] = execute_penalty(
            away_prob, away_name, away_penalties_array, match_data['away_penalties']
        )

        # Standard best-of-5 logic
        if 2 < turns < PENALTY_DEFAULT_TURNS:
            home_remaining = PENALTY_DEFAULT_TURNS - turns
            away_remaining = PENALTY_DEFAULT_TURNS - turns
            if match_data['home_penalties'] > match_data['away_penalties'] + away_remaining or \
               match_data['away_penalties'] > match_data['home_penalties'] + home_remaining:
                penalty_kick_over = True

        # Sudden death logic
        if turns >= PENALTY_DEFAULT_TURNS:
            if match_data['home_penalties'] != match_data['away_penalties']:
                penalty_kick_over = True

        turns += 1
        time.sleep(SLEEP_TIME)


def simulate_match(home_iso: str, away_iso: str, is_extra_time: bool) -> Dict[str, Any]:
    """Simulates a full match between two teams."""
    match_data = {'home_goals': 0, 'away_goals': 0, 'home_penalties': None, 'away_penalties': None}
    
    home_teams = get_team_by_id(home_iso)
    away_teams = get_team_by_id(away_iso)
    
    if not home_teams or not away_teams:
        raise ValueError(f"Team not found: {home_iso if not home_teams else away_iso}")
        
    home_team = home_teams[0]
    away_team = away_teams[0]
    home_name = home_team['nation_name']
    away_name = away_team['nation_name']

    home_prob, away_prob = calculate_winner_probability(
        home_team['fifa_nation_rank'], away_team['fifa_nation_rank']
    )
    
    print(f" MATCH START: {home_name} vs {away_name} ".center(LOG_LENGTH, ':'))
    simulate_match_time(1, 90, home_prob, away_prob, home_name, away_name, match_data)

    if is_extra_time and match_data['home_goals'] == match_data['away_goals']:
        print(f" EXTRA TIME: {home_name} vs {away_name} ".center(LOG_LENGTH, ':'))
        simulate_extra_match(home_prob, away_prob, home_team, away_team, match_data)

    penalty_home = f"[{match_data['home_penalties']}]" if match_data['home_penalties'] is not None else ''
    penalty_away = f"[{match_data['away_penalties']}]" if match_data['away_penalties'] is not None else ''
    
    print(
        f" MATCH FINISHED: {home_name} {match_data['home_goals']} {penalty_home} - "
        f"{away_name} {match_data['away_goals']} {penalty_away} ".center(LOG_LENGTH, ':')
    )
    
    return {
        'local': match_data['home_goals'],
        'visita': match_data['away_goals'],
        'penales_local': match_data['home_penalties'],
        'penales_visita': match_data['away_penalties']
    }


def simulate_extra_match(home_prob: float, away_prob: float, home_team: Dict[str, Any], away_team: Dict[str, Any], match_data: Dict[str, Any]) -> None:
    """Simulates extra time and penalties if needed."""
    simulate_match_time(91, 120, home_prob, away_prob, home_team['nation_name'], away_team['nation_name'], match_data)
    
    if match_data['home_goals'] == match_data['away_goals']:
        simulate_penalty_shots(home_prob, away_prob, home_team['nation_name'], away_team['nation_name'], match_data)
