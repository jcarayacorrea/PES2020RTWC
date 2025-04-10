import random
import time
from utils import medium_difference, high_difference, extreme_difference, ultra_difference, getTeamById

SLEEP_TIME = 0.1
GOAL = 'O'
NO_GOAL = 'X'
HOME_GOAL = 'L'
AWAY_GOAL = 'V'
STEP = '-'
GOAL_PRBLTY = 0.03
PENALTY_DEFAULT_TURNS = 5


def calculate_probability(winner_rank, loser_rank):
    """Calculates the probability of the lesser ranked team winning."""
    diff_functions = [medium_difference, high_difference, extreme_difference, ultra_difference, lambda x, y: True]
    probabilities = [(0.65, 0.35), (0.7, 0.3), (0.8, 0.2), (0.9, 0.1), (0.6, 0.4)]

    for diff_func, probability in zip(diff_functions, probabilities):
        if diff_func(winner_rank, loser_rank):
            return probability


def calculate_winner_probability(home_rank, guest_rank):
    if home_rank < guest_rank:
        # home team is likely to win
        return calculate_probability(home_rank, guest_rank)
    elif home_rank > guest_rank:
        # guest team is likely to win, reverse the probability
        home_prob, guest_prob = calculate_probability(guest_rank, home_rank)
        return guest_prob, home_prob
    else:
        # equal probabilities for both if ranks are same
        return 0.5, 0.5


def display_event(tiempo_transcurrido, nombre, goles_local, goles_visitante, penales=[], tipo="Gol"):
    def gol_display():
        print(f'{tipo} {nombre} ({tiempo_transcurrido}) {goles_local} - {goles_visitante}\n')

    def penales_display():
        print(f'{tipo} {nombre}  {penales[:-5]}\n')

    def minuto_display():
        print(f'Minuto ({tiempo_transcurrido})\n')

    event_types = {
        'Gol': gol_display,
        'Penales': penales_display,
        'Minuto': minuto_display
    }

    event_types[tipo]()


def process_match_event(event_time, home_goal_probability, away_goal_probability, home_team_name, away_team_name,
                        home_team_goals, away_team_goals):
    event = random.choices([HOME_GOAL, AWAY_GOAL, STEP],
                           [home_goal_probability * GOAL_PRBLTY, away_goal_probability * GOAL_PRBLTY,
                            1 - (home_goal_probability * GOAL_PRBLTY) + (away_goal_probability * GOAL_PRBLTY)])[0]
    if event in [HOME_GOAL, AWAY_GOAL]:
        if event == HOME_GOAL:
            home_team_goals += 1
            team = home_team_name
        else:
            away_team_goals += 1
            team = away_team_name
        display_event(event_time, team, home_team_goals, away_team_goals)
        return home_team_goals, away_team_goals
    else:
        display_event(event_time, home_team_name, home_team_goals, away_team_goals, tipo="Minuto")
        return home_team_goals, away_team_goals


def simulate_match_time(match_duration, home_goal_probability, away_goal_probability, home_team_name, away_team_name,
                        home_team_goals=0, away_team_goals=0):
    event_time = 1
    while event_time <= match_duration:
        home_team_goals, away_team_goals = process_match_event(event_time, home_goal_probability, away_goal_probability,
                                                               home_team_name, away_team_name, home_team_goals,
                                                               away_team_goals)
        event_time += 1
        time.sleep(SLEEP_TIME)
    return home_team_goals, away_team_goals


def execute_penalty(probability, name, penalty_array, penalties):
    event = random.choices([GOAL, NO_GOAL], [probability, 1 - probability])[0]
    penalty_array.append(event)
    if event == 'O':
        penalties += 1
    display_event(0, name, None, None, penalty_array, tipo="Penalties")
    time.sleep(SLEEP_TIME)
    return event, penalties


def simulate_penalty_shots(probabilidad_local, probabilidad_visitante, nombre_local, nombre_visita):
    local_penalties_array = []
    away_penalties_array = []
    local_penalties = 0
    away_penalties = 0
    penalties_turns = 1
    penalty_kick_over = False
    print(f" PENALES {nombre_local} - {nombre_visita}")

    while not penalty_kick_over:
        _, local_penalties = execute_penalty(probabilidad_local, nombre_local, local_penalties_array, local_penalties)
        _, away_penalties = execute_penalty(probabilidad_visitante, nombre_visita, away_penalties_array, away_penalties)

        if penalties_turns > 2 and penalties_turns < PENALTY_DEFAULT_TURNS:
            if (PENALTY_DEFAULT_TURNS - local_penalties) - (PENALTY_DEFAULT_TURNS - away_penalties) > \
                    (PENALTY_DEFAULT_TURNS - penalties_turns):
                penalty_kick_over = True

        if penalties_turns >= PENALTY_DEFAULT_TURNS:
            if local_penalties != away_penalties:
                penalty_kick_over = True

        penalties_turns += 1
        time.sleep(SLEEP_TIME)
    return local_penalties, away_penalties


def simulate_match(home_team_id, away_team_id, is_extra_time):
    home_team = getTeamById(home_team_id)
    away_team = getTeamById(away_team_id)
    home_nation_name = home_team[0]['nation_name']
    away_nation_name = away_team[0]['nation_name']
    home_penalties = None
    away_penalties = None

    home_probability, away_probability = calculate_winner_probability(home_team[0]['fifa_nation_rank'],
                                                                      away_team[0]['fifa_nation_rank'])
    print(f' INICIO DE PARTIDO {home_nation_name} - {away_nation_name}'.center(50, ':'))
    home_goals, away_goals = simulate_match_time(90, home_probability, away_probability, home_team[0]['nation_name'],
                                                 away_team[0]['nation_name'])

    is_draw = home_goals == away_goals

    if is_extra_time and is_draw:
        print(f' TIEMPO EXTRA {home_nation_name} - {away_nation_name}'.center(100, ':'))
        home_goals, away_goals, home_penalties, away_penalties = simulate_extra_match(home_probability,
                                                                                      away_probability, home_team,
                                                                                      away_team,
                                                                                      home_goals, away_goals)
    print(
        f"FIN PARTIDO {home_nation_name} {home_goals} [{home_penalties}] - {away_nation_name} {away_goals} [{away_penalties}]".center(
            100, ':'))
    return {'local': home_goals, 'visita': away_goals, 'penales_local': home_penalties,
            'penales_visita': away_penalties}


def simulate_extra_match(home_probability, away_probability, home_team, away_team, home_goals, away_goals):
    home_goals, away_goals = simulate_match_time(30, home_probability, away_probability, home_team[0]['nation_name'],
                                                 away_team[0]['nation_name'])
    return home_goals, away_goals if home_goals != away_goals else simulate_penalty_shots(home_probability,
                                                                                          away_probability,
                                                                                          home_team[0]['nation_name'],
                                                                                          away_team[0]['nation_name'])
