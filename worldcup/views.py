import random
from typing import List, Dict, Any, Tuple, Optional
from functools import reduce

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

from Global_Variables import GROUP_RANGE, GROUP_KEYS
from fixtures import create_playoff_matches, get_zone_data
from utils import get_teams_main_draw, get_teams_playoff

GROUP_COUNT = len(GROUP_KEYS)
MIN_TEAMS = 1
MAX_TEAMS = 2


def main_draw(request: HttpRequest) -> HttpResponse:
    """Renders the main draw page with all qualified teams."""
    teams = get_teams_main_draw()
    confederations = ['CONMEBOL', 'UEFA', 'CONCACAF', 'OFC', 'CAF', 'AFC']
    context = {'teams': teams, 'confederations': confederations, 'range': GROUP_RANGE[0:4]}

    return render(request, 'worldcup/maindraw.html', context)


def get_playoff_context_data() -> Dict[str, Any]:
    """Helper to prepare context data for the playoff page."""
    playoff_data = get_zone_data('P', 'FIFA', 'playoff')
    return {
        'teams': get_teams_playoff(),
        'fixture': playoff_data['fixtures']
    }


def playoff(request: HttpRequest) -> HttpResponse:
    """Renders the current playoff state."""
    context = get_playoff_context_data()
    return render(request, 'worldcup/playoff.html', context)


def shuffle_teams_and_assign_to_context(groups: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
    """Shuffles teams within each group and prepares them for the context."""
    context = {}
    for zone_key in GROUP_KEYS:
        zone_teams = groups[zone_key]
        random.shuffle(zone_teams)
        context[f'zone{zone_key}'] = zone_teams
    return context


def draw_main_button(request: HttpRequest) -> HttpResponse:
    """Handles the main draw generation logic with retries on failure."""
    if request.method == 'GET':
        confederations = ['CONMEBOL', 'UEFA', 'CONCACAF', 'OFC', 'CAF', 'AFC']
        teams = get_teams_main_draw()
        context = {'teams': teams, 'confederations': confederations}
        
        # Iterative retry instead of recursion to avoid potential RecursionError
        max_attempts = 100
        for _ in range(max_attempts):
            try:
                groups = perform_draw(teams)
                zone_context = shuffle_teams_and_assign_to_context(groups)
                context.update(zone_context)
                break
            except (ValueError, IndexError):
                continue
        else:
            # If it fails after max_attempts, we should probably handle it gracefully
            return HttpResponse("Failed to generate a valid draw after multiple attempts", status=500)
            
        return render(request, 'worldcup/maindraw.html', context)
    return redirect('maindraw')


def prepare_playoff_data() -> Tuple[List[Dict[str, Any]], Any]:
    """Simulates the playoff draw and saves it to the database."""
    teams = get_teams_playoff()
    zones = perform_playoff_draw(teams)
    for zone in zones:
        random.shuffle(zone)
    
    create_playoff_matches(teams, *zones)
    playoff_data = get_zone_data('P', 'FIFA', 'playoff')

    return teams, playoff_data['fixtures']


def get_playoff_page(request: HttpRequest) -> HttpResponse:
    """Generates a new playoff draw and renders the page."""
    if request.method == 'GET':
        playoff_teams, playoff_fixtures = prepare_playoff_data()
        context = {'teams': playoff_teams, 'fixture': playoff_fixtures}
        return render(request, 'worldcup/playoff.html', context)
    return redirect('playoff')


def perform_playoff_draw(teams: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], ...]:
    """Splits playoff teams into three pools."""
    pools = []
    num_pools = 3
    teams_per_pool = 6

    for i in range(num_pools):
        start = i * teams_per_pool
        end = start + teams_per_pool
        pool = teams[start:end]
        random.shuffle(pool)
        pools.append(pool)

    return tuple(pools)


def perform_draw(teams: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Performs the main World Cup group stage draw."""
    groups = {key: [] for key in GROUP_KEYS}
    
    # Pool 1: Seeded teams (first 8)
    seeded_teams = teams[0:8].copy()
    random.shuffle(seeded_teams)
    for key, team in zip(GROUP_KEYS, seeded_teams):
        groups[key].append(team)

    # Pools 2, 3, 4 (teams 8-15, 16-23, 24-31)
    pools = [teams[8:16], teams[16:24], teams[24:32]]
    for pool_idx, pool in enumerate(pools):
        shuffled_pool = pool.copy()
        random.shuffle(shuffled_pool)
        max_group_size = pool_idx + 2
        for team in shuffled_pool:
            set_team_position(
                team, 
                groups, 
                teams_count_in_conf=count_teams_in_conf(team['conf_name'], teams),
                max_group_size=max_group_size
            )
            
    return groups


def set_team_position(team: Dict[str, Any], groups: Dict[str, List[Dict[str, Any]]], 
                      teams_count_in_conf: int, max_group_size: int) -> None:
    """Finds an available group for a team based on confederation limits."""
    available_zones = []
    for zone in GROUP_KEYS:
        is_conf_limit_reached = is_conf_limit_reached_in_group(team['conf_name'], groups[zone], teams_count_in_conf)
        is_group_full = len(groups[zone]) == max_group_size
        
        if not is_conf_limit_reached and not is_group_full:
            available_zones.append(zone)
            
    if not available_zones:
        # Raising an error to trigger a retry in draw_main_button
        raise ValueError(f"No available zones for team {team.get('nation_name')} from {team['conf_name']}")
        
    chosen_zone = random.choice(available_zones)
    groups[chosen_zone].append(team)


def is_conf_limit_reached_in_group(conf_name: str, group_list: List[Dict[str, Any]], total_teams_in_conf: int) -> bool:
    """Checks if the confederation limit for a group has been reached."""
    count_in_group = len([team for team in group_list if team['conf_name'] == conf_name])
    if total_teams_in_conf <= GROUP_COUNT:
        return count_in_group >= MIN_TEAMS
    else:
        return count_in_group >= MAX_TEAMS


def count_teams_in_conf(conf_name: str, team_list: List[Dict[str, Any]]) -> int:
    """Counts how many teams from a specific confederation are in the list."""
    return len([team for team in team_list if team['conf_name'] == conf_name])
