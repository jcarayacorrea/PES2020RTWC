from typing import List, Dict, Any, Tuple
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from Global_Variables import GROUP_KEYS, GROUP_RANGE
from main.services import ConfederationService
from fixtures import create_playoff_matches_uefa, get_zone_data
from utils import get_uefa_teams_playoff
import random

CONF_NAME = 'UEFA'
service = ConfederationService(CONF_NAME)


def final_round(request: HttpRequest) -> HttpResponse:
    """Renders the final round state for UEFA."""
    context = service.get_round_context('final', GROUP_KEYS, team_size=5, group_range=GROUP_RANGE)
    return render(request, 'europa/finalround.html', context)


def first_round(request: HttpRequest) -> HttpResponse:
    """Renders the first round state for UEFA."""
    context = service.get_round_context('first', GROUP_KEYS[0:5], team_size=5, group_range=GROUP_RANGE)
    return render(request, 'europa/fstround.html', context)


def teams(request: HttpRequest) -> HttpResponse:
    """Renders the list of UEFA teams."""
    context = {'teams': service.get_all_teams()}
    return render(request, 'europa/teamlist.html', context)


def update_progress(request: HttpRequest, code: str, stage: str) -> HttpResponse:
    """Updates the stage progress for a team."""
    if request.method == 'POST':
        service.update_team_progress(code, stage)
    return redirect('europa.teams')


def first_round_button(request: HttpRequest) -> HttpResponse:
    """Generates the draw and fixtures for the first round."""
    if request.method == 'GET':
        service.perform_draw('first', pools_count=5, teams_per_pool=5, home_away=True)
        return first_round(request)
    return redirect('europa.fstround')


def final_round_button(request: HttpRequest) -> HttpResponse:
    """Generates the draw and fixtures for the final round."""
    if request.method == 'GET':
        service.perform_draw('final', pools_count=5, teams_per_pool=8, home_away=True)
        return final_round(request)
    return redirect('europa.finalround')


def euro_playoff(request: HttpRequest) -> HttpResponse:
    """Renders the UEFA playoff state."""
    context = get_playoff_context_data()
    return render(request, 'europa/playoff.html', context)


def get_playoff_page(request: HttpRequest) -> HttpResponse:
    """Generates a new UEFA playoff draw and renders the page."""
    if request.method == 'GET':
        playoff_teams, playoff_fixtures = prepare_playoff_data()
        context = {'teams': playoff_teams, 'fixture': playoff_fixtures}
        return render(request, 'europa/playoff.html', context)
    return redirect('europa.playoff')


def get_playoff_context_data() -> Dict[str, Any]:
    """Helper to prepare context data for the playoff page."""
    playoff_data = get_zone_data('P', CONF_NAME, 'playoff')
    return {
        'teams': get_uefa_teams_playoff(CONF_NAME),
        'fixture': playoff_data['fixtures']
    }


def playoff_draw(teams: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], ...]:
    """Splits playoff teams into pools."""
    pools = []
    num_pools = 2
    teams_per_pool = 4

    for i in range(num_pools):
        start = i * teams_per_pool
        end = start + teams_per_pool
        pool = teams[start:end]
        random.shuffle(pool)
        pools.append(pool)

    return tuple(pools)


def prepare_playoff_data() -> Tuple[List[Dict[str, Any]], Any]:
    """Simulates the UEFA playoff draw and saves it to the database."""
    teams = get_uefa_teams_playoff(CONF_NAME)
    zones = playoff_draw(teams)
    for zone in zones:
        random.shuffle(zone)
    create_playoff_matches_uefa(teams, *zones)
    playoff_data = get_zone_data('P', CONF_NAME, 'playoff')

    return teams, playoff_data['fixtures']


