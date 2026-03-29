from typing import List, Dict, Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from Global_Variables import GROUP_KEYS, GROUP_RANGE
from main.services import ConfederationService

CONF_NAME = 'AFC'
service = ConfederationService(CONF_NAME)


def final_round(request: HttpRequest) -> HttpResponse:
    """Renders the final round state for AFC."""
    context = service.get_round_context('final', GROUP_KEYS[0:4], team_size=5, group_range=GROUP_RANGE)
    return render(request, 'asia/finalround.html', context)


def third_round(request: HttpRequest) -> HttpResponse:
    """Renders the third round state for AFC."""
    context = service.get_round_context('third', GROUP_KEYS[0:6], team_size=4, group_range=GROUP_RANGE[0:4])
    return render(request, 'asia/thrround.html', context)


def second_round(request: HttpRequest) -> HttpResponse:
    """Renders the second round state for AFC."""
    context = service.get_round_context('second', GROUP_KEYS[0:6], team_size=4, group_range=GROUP_RANGE[0:4])
    return render(request, 'asia/sndround.html', context)


def first_round(request: HttpRequest) -> HttpResponse:
    """Renders the first round state for AFC."""
    context = service.get_round_context('first', GROUP_KEYS[0:1], team_size=4, group_range=GROUP_RANGE[0:4])
    return render(request, 'asia/fstround.html', context)


def teams(request: HttpRequest) -> HttpResponse:
    """Renders the list of AFC teams."""
    context = {'teams': service.get_all_teams()}
    return render(request, 'asia/teamlist.html', context)


def update_progress(request: HttpRequest, code: str, stage: str) -> HttpResponse:
    """Updates the stage progress for a team."""
    if request.method == 'POST':
        service.update_team_progress(code, stage)
    return redirect('asia.teams')


def first_round_button(request: HttpRequest) -> HttpResponse:
    """Generates the draw and fixtures for the first round."""
    if request.method == 'GET':
        service.perform_draw('first', pools_count=4, teams_per_pool=1, home_away=False)
        return first_round(request)
    return redirect('asia.fstround')


def second_round_button(request: HttpRequest) -> HttpResponse:
    """Generates the draw and fixtures for the second round."""
    if request.method == 'GET':
        service.perform_draw('second', pools_count=4, teams_per_pool=6, home_away=True)
        return second_round(request)
    return redirect('asia.sndround')


def third_round_button(request: HttpRequest) -> HttpResponse:
    """Generates the draw and fixtures for the third round."""
    if request.method == 'GET':
        service.perform_draw('third', pools_count=4, teams_per_pool=6, home_away=True)
        return third_round(request)
    return redirect('asia.thrround')


def final_round_button(request: HttpRequest) -> HttpResponse:
    """Generates the draw and fixtures for the final round."""
    if request.method == 'GET':
        service.perform_draw('final', pools_count=5, teams_per_pool=4, home_away=True)
        return final_round(request)
    return redirect('asia.finalround')