from typing import List, Dict, Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from Global_Variables import GROUP_RANGE, GROUP_KEYS
from main.services import ConfederationService
from fixtures import get_zone_data
from utils import db_conexion, get_team_by_id

CONF_NAME = 'OFC'
service = ConfederationService(CONF_NAME)


def final_round(request: HttpRequest) -> HttpResponse:
    """Renders the final round state for OFC."""
    context = service.get_round_context('final', GROUP_KEYS[0:2], team_size=4, group_range=GROUP_RANGE[0:4])
    fixture = get_zone_data('MD', 'OFC', 'final')
    context['fixture'] = fixture['fixtures']

    return render(request, 'oceania/finalround.html', context)


def first_round(request: HttpRequest) -> HttpResponse:
    """Renders the first round state for OFC."""
    context = service.get_round_context('first', GROUP_KEYS[0:1], team_size=5, group_range=GROUP_RANGE)
    return render(request, 'oceania/fstround.html', context)


def teams(request: HttpRequest) -> HttpResponse:
    """Renders the list of OFC teams."""
    context = {'teams': service.get_all_teams()}
    return render(request, 'oceania/teamlist.html', context)


def update_progress(request: HttpRequest, code: str, stage: str) -> HttpResponse:
    """Updates the stage progress for a team."""
    if request.method == 'POST':
        service.update_team_progress(code, stage)
    return redirect('oceania.teams')


def first_round_button(request: HttpRequest) -> HttpResponse:
    """Generates the draw and fixtures for the first round."""
    if request.method == 'GET':
        service.perform_draw('first', pools_count=5, teams_per_pool=1, home_away=False)
        return first_round(request)
    return redirect('oceania.fstround')


def final_round_button(request: HttpRequest) -> HttpResponse:
    """Generates the draw and fixtures for the final round."""
    if request.method == 'GET':
        service.perform_draw('final', pools_count=4, teams_per_pool=2, home_away=True)
        return final_round(request)
    return redirect('oceania.finalround')


def set_home_final_team(request: HttpRequest) -> HttpResponse:
    """Manually sets the home team for the OFC final."""
    db = db_conexion()
    team_id = request.GET.get('team')
    if not team_id:
        return redirect('oceania.finalround')
    team = get_team_by_id(team_id)
    db.get_collection('Fixtures').update_many(
        {'conf': 'OFC', 'zone': 'MD', 'round': 'final'},
        {'$set': {
            'fixtures.mainDraw.match1.played': False,
            'fixtures.mainDraw.match1.homeTeam.team': team[0],
            'fixtures.mainDraw.match1.homeTeam.goals': None,
            'fixtures.mainDraw.match1.homeTeam.penalties': None
        }}
    )
    return final_round(request)


def set_away_final_team(request: HttpRequest) -> HttpResponse:
    """Manually sets the away team for the OFC final."""
    db = db_conexion()
    team_id = request.GET.get('team')
    if not team_id:
        return redirect('oceania.finalround')
    team = get_team_by_id(team_id)
    db.get_collection('Fixtures').update_one(
        {'conf': 'OFC', 'zone': 'MD', 'round': 'final'},
        {'$set': {
            'fixtures.mainDraw.match1.played': False,
            'fixtures.mainDraw.match1.awayTeam.team': team[0],
            'fixtures.mainDraw.match1.awayTeam.goals': None,
            'fixtures.mainDraw.match1.awayTeam.penalties': None
        }}
    )
    return final_round(request)
