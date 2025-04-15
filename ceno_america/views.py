import random

from django.shortcuts import render, redirect

from Global_Variables import GROUP_CODES, GROUP_RANGE
from draw import get_zone_with_teams_of_size, round_draw
from fixtures import getZoneData, create_fixture
from utils import updateStage, getTeams, getTeamsFinalRound, getTeamsFirstRound

CONF_NAME = 'CONCACAF'


# Create your views here.
def finalround(request):
    context = {}
    round_name = 'final'
    context['teams'] = getTeamsFinalRound(conf_name=CONF_NAME)
    for zone_code in GROUP_CODES[0:3]:
        teams = get_zone_with_teams_of_size(zone_code, CONF_NAME, round_name, team_size=5)
        if teams is not None:
            context[f'zone{zone_code}'] = teams
    context['range'] = GROUP_RANGE
    return render(request, 'ncamerica/finalround.html', context)


def firstround(request):
    context = {}
    round_name = 'first'
    context['teams'] = getTeamsFirstRound(conf_name=CONF_NAME)
    for zone_code in GROUP_CODES[0:5]:
        teams = get_zone_with_teams_of_size(zone_code, CONF_NAME, round_name, team_size=5)
        if teams is not None:
            context[f'zone{zone_code}'] = teams
    context['range'] = GROUP_RANGE
    return render(request, 'ncamerica/fstround.html', context)


def teams(request):
    context = {}
    context['teams'] = getTeams(conf_name='CONCACAF')
    return render(request, 'ncamerica/teamlist.html', context)


def updateProgress(request, id, stage):
    if request.method == 'POST':
        updateStage(id, stage)
    return redirect('ncamerica.teams')


def firstRoundButton(request):
    if request.method == 'GET':
        context = {}
        teams_for_match = getTeamsFirstRound(CONF_NAME)
        context['teams'] = teams_for_match
        zones = round_draw(teams_for_match, pools_count=5, teams_per_pool=5)
        for zone_idx, zone in enumerate(zones, start=1):
            random.shuffle(zone)
            create_fixture(zone, True, chr(ord('A') + zone_idx - 1), CONF_NAME, 'first')
            context[f'zone{zone_idx}'] = zone
    return firstround(request)


def finalRoundButton(request):
    if request.method == 'GET':
        context = {}
        teams_for_match = getTeamsFinalRound(CONF_NAME)
        context['teams'] = teams_for_match
        zones = round_draw(teams_for_match, pools_count=5, teams_per_pool=3)
        for zone_idx, zone in enumerate(zones, start=1):
            random.shuffle(zone)
            create_fixture(zone, True, chr(ord('A') + zone_idx - 1), CONF_NAME, 'final')
            context[f'zone{zone_idx}'] = zone
        return finalround(request)
