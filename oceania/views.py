from typing import List, Dict, Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from Global_Variables import GROUP_RANGE, GROUP_KEYS
from main.services import get_service
from fixtures import get_zone_data

CONF_NAME = 'OFC'


def _service():
    return get_service(CONF_NAME)


def final_round(request: HttpRequest) -> HttpResponse:
    """Renders the final round state for OFC."""
    context = _service().get_round_context('final', GROUP_KEYS[0:2], team_size=4, group_range=GROUP_RANGE[0:4])
    fixture = get_zone_data('MD', 'OFC', 'final')
    context['fixture'] = fixture['fixtures']

    return render(request, 'oceania/finalround.html', context)


def first_round(request: HttpRequest) -> HttpResponse:
    """Renders the first round state for OFC."""
    context = _service().get_round_context('first', GROUP_KEYS[0:1], team_size=5, group_range=GROUP_RANGE)
    return render(request, 'oceania/fstround.html', context)


def teams(request: HttpRequest) -> HttpResponse:
    """Renders the list of OFC teams."""
    context = {'teams': _service().get_all_teams()}
    return render(request, 'oceania/teamlist.html', context)


def update_progress(request: HttpRequest, code: str, stage: str) -> HttpResponse:
    """Updates the stage progress for a team."""
    if request.method == 'POST':
        _service().update_team_progress(code, stage)
    return redirect('oceania.teams')


def first_round_button(request: HttpRequest) -> HttpResponse:
    """Generates the draw and fixtures for the first round."""
    if request.method == 'GET':
        _service().perform_draw('first', pools_count=5, teams_per_pool=1, home_away=False)
        return first_round(request)
    return redirect('oceania.fstround')


def final_round_button(request: HttpRequest) -> HttpResponse:
    """Generates the draw and fixtures for the final round."""
    if request.method == 'GET':
        _service().perform_draw('final', pools_count=4, teams_per_pool=2, home_away=True)
        return final_round(request)
    return redirect('oceania.finalround')


def set_home_final_team(request: HttpRequest) -> HttpResponse:
    """Manually sets the home team for the OFC final."""
    team_id = request.GET.get('team')
    if not team_id:
        return redirect('oceania.finalround')
    _service().set_final_team('MD', 'final', 'mainDraw', 'home', team_id)
    return final_round(request)


def set_away_final_team(request: HttpRequest) -> HttpResponse:
    """Manually sets the away team for the OFC final."""
    team_id = request.GET.get('team')
    if not team_id:
        return redirect('oceania.finalround')
    _service().set_final_team('MD', 'final', 'mainDraw', 'away', team_id)
    return final_round(request)
