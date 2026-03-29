import random
from typing import List, Dict, Any, Tuple
from operator import itemgetter

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from Global_Variables import GROUP_RANGE
from utils import get_teams_copa_america
from main.services import ConfederationService

CONF_NAME = 'CONMEBOL'
service = ConfederationService(CONF_NAME)

CONMEBOL_SEEDS_COUNT = 2
CONCACAF_SEEDS_COUNT = 2
REST_TEAMS_COUNT = 10
POOL_SIZE = 4


def teams(request: HttpRequest) -> HttpResponse:
    """Renders the list of CONMEBOL teams."""
    context = {'teams': service.get_all_teams()}
    return render(request, 'sudamerica/teamlist.html', context)


def copa_america(request: HttpRequest) -> HttpResponse:
    """Renders the Copa America state."""
    context = {
        'teams': get_teams_copa_america(),
        'range': GROUP_RANGE[0:4]
    }
    return render(request, 'sudamerica/copaamerica.html', context)


def update_progress(request: HttpRequest, code: str, stage: str) -> HttpResponse:
    """Updates the stage progress for a team."""
    if request.method == 'POST':
        service.update_team_progress(code, stage)
    return redirect('sudamerica.finalround')


def copa_america_button(request: HttpRequest) -> HttpResponse:
    """Generates the draw for Copa America."""
    if request.method == 'GET':
        all_teams = get_teams_copa_america()
        zones = perform_copa_america_draw(all_teams)
        for zone in zones:
            random.shuffle(zone)
        context = {
            'teams': all_teams,
            'zoneA': zones[0],
            'zoneB': zones[1],
            'zoneC': zones[2],
            'zoneD': zones[3],
        }

        return render(request, 'sudamerica/copaamerica.html', context)
    return redirect('sudamerica.copaamerica')


def extract_teams_by_federation(teams_list: List[Dict[str, Any]], federation: str) -> List[Dict[str, Any]]:
    """Filters teams by their confederation name."""
    return [team for team in teams_list if team['conf_name'] == federation]


def create_zone(seed_list: List[Dict[str, Any]], pool2: List[Dict[str, Any]], pool3: List[Dict[str, Any]], pool4: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Creates a group zone by picking one team from each seed/pool list."""
    return [
        seed_list.pop(),
        pool2.pop(),
        pool3.pop(),
        pool4.pop()
    ]


def shuffle_lists(*args: List[Any]) -> None:
    """Shuffles multiple lists in place."""
    for arg in args:
        random.shuffle(arg)


def perform_copa_america_draw(all_teams: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], ...]:
    """Performs the Copa America draw logic."""
    sudamerica = extract_teams_by_federation(all_teams, 'CONMEBOL')
    ncamerica = extract_teams_by_federation(all_teams, 'CONCACAF')

    # Create seed lists and rest of teams list
    sud_seed = sudamerica[:CONMEBOL_SEEDS_COUNT]
    nc_seed = ncamerica[:CONCACAF_SEEDS_COUNT]
    
    rest_teams = sorted(
        sudamerica[CONMEBOL_SEEDS_COUNT:REST_TEAMS_COUNT] + ncamerica[CONCACAF_SEEDS_COUNT:6],
        key=itemgetter('fifa_nation_rank')
    )

    # Split rest_teams into pools
    pool2 = rest_teams[0:POOL_SIZE]
    pool3 = rest_teams[POOL_SIZE:POOL_SIZE*2]
    pool4 = rest_teams[POOL_SIZE*2:POOL_SIZE*3]

    # Shuffle lists
    shuffle_lists(sud_seed, nc_seed, pool2, pool3, pool4)

    # Creating zones
    zone1 = create_zone(sud_seed, pool2, pool3, pool4)
    zone2 = create_zone(nc_seed, pool2, pool3, pool4)
    zone3 = create_zone(nc_seed, pool2, pool3, pool4)
    zone4 = create_zone(sud_seed, pool2, pool3, pool4)

    return zone1, zone2, zone3, zone4
