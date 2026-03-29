from typing import List, Dict, Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from Global_Variables import GROUP_KEYS, GROUP_RANGE
from main.services import ConfederationService

CONF_NAME = 'CONCACAF'
service = ConfederationService(CONF_NAME)


def final_round(request: HttpRequest) -> HttpResponse:
    """Renders the final round state for CONCACAF."""
    context = service.get_round_context('final', GROUP_KEYS[0:3], team_size=5, group_range=GROUP_RANGE)
    return render(request, 'ncamerica/finalround.html', context)


def first_round(request: HttpRequest) -> HttpResponse:
    """Renders the first round state for CONCACAF."""
    context = service.get_round_context('first', GROUP_KEYS[0:5], team_size=5, group_range=GROUP_RANGE)
    return render(request, 'ncamerica/fstround.html', context)


def teams(request: HttpRequest) -> HttpResponse:
    """Renders the list of CONCACAF teams."""
    context = {'teams': service.get_all_teams()}
    return render(request, 'ncamerica/teamlist.html', context)


def update_progress(request: HttpRequest, code: str, stage: str) -> HttpResponse:
    """Updates the stage progress for a team."""
    if request.method == 'POST':
        service.update_team_progress(code, stage)
    return redirect('ncamerica.teams')


def first_round_button(request: HttpRequest) -> HttpResponse:
    """Generates the draw and fixtures for the first round."""
    if request.method == 'GET':
        service.perform_draw('first', pools_count=5, teams_per_pool=5, home_away=True)
        return first_round(request)
    return redirect('ncamerica.fstround')


def final_round_button(request: HttpRequest) -> HttpResponse:
    """Generates the draw and fixtures for the final round."""
    if request.method == 'GET':
        service.perform_draw('final', pools_count=5, teams_per_pool=3, home_away=True)
        return final_round(request)
    return redirect('ncamerica.finalround')
