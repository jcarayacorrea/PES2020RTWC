from typing import List, Dict, Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from Global_Variables import GROUP_KEYS, GROUP_RANGE
from main.services import ConfederationService

CONF_NAME = 'CAF'
service = ConfederationService(CONF_NAME)


def final_round(request: HttpRequest) -> HttpResponse:
    """Renders the final round state for CAF."""
    context = service.get_round_context('final', GROUP_KEYS[0:5], team_size=5, group_range=GROUP_RANGE)
    return render(request, 'africa/finalround.html', context)


def third_round(request: HttpRequest) -> HttpResponse:
    """Renders the third round state for CAF."""
    context = service.get_round_context('third', GROUP_KEYS[0:5], team_size=4, group_range=GROUP_RANGE[0:4])
    return render(request, 'africa/thrround.html', context)


def second_round(request: HttpRequest) -> HttpResponse:
    """Renders the second round state for CAF."""
    context = service.get_round_context('second', GROUP_KEYS[0:5], team_size=4, group_range=GROUP_RANGE[0:4])
    return render(request, 'africa/sndround.html', context)


def first_round(request: HttpRequest) -> HttpResponse:
    """Renders the first round state for CAF."""
    context = service.get_round_context('first', GROUP_KEYS[0:3], team_size=4, group_range=GROUP_RANGE[0:4])
    return render(request, 'africa/fstround.html', context)


def teams(request: HttpRequest) -> HttpResponse:
    """Renders the list of CAF teams."""
    context = {'teams': service.get_all_teams()}
    return render(request, 'africa/teamlist.html', context)


def update_progress(request: HttpRequest, code: str, stage: str) -> HttpResponse:
    """Updates the stage progress for a team."""
    if request.method == 'POST':
        service.update_team_progress(code, stage)
    return redirect('africa.teams')


def first_round_button(request: HttpRequest) -> HttpResponse:
    """Generates the draw and fixtures for the first round."""
    if request.method == 'GET':
        service.perform_draw('first', pools_count=4, teams_per_pool=3, home_away=False)
        return first_round(request)
    return redirect('africa.fstround')


def second_round_button(request: HttpRequest) -> HttpResponse:
    """Generates the draw and fixtures for the second round."""
    if request.method == 'GET':
        service.perform_draw('second', pools_count=4, teams_per_pool=5, home_away=True)
        return second_round(request)
    return redirect('africa.sndround')


def third_round_button(request: HttpRequest) -> HttpResponse:
    """Generates the draw and fixtures for the third round."""
    if request.method == 'GET':
        service.perform_draw('third', pools_count=4, teams_per_pool=5, home_away=True)
        return third_round(request)
    return redirect('africa.thrround')


def final_round_button(request: HttpRequest) -> HttpResponse:
    """Generates the draw and fixtures for the final round."""
    if request.method == 'GET':
        service.perform_draw('final', pools_count=5, teams_per_pool=5, home_away=True)
        return final_round(request)
    return redirect('africa.finalround')


def team_list_filter(text: str) -> List[Dict[str, Any]]:
    """Filters CAF teams by name."""
    return service.filter_teams(text)