import random

from django.shortcuts import render, redirect

from draw import get_zone_with_teams_of_size, round_draw
from utils import db_conexion, getTeams, updateStage, getTeamsFirstRound, getTeamsSecondRound, getTeamsThirdRound, \
    getTeamsFinalRound, GROUP_CODES, GROUP_RANGE
from fixtures import create_fixture, getZoneData

CONF_NAME = 'AFC'


# Create your views here.
def finalround(request):
    context = {}
    round_name = 'final'
    context['teams'] = getTeamsFinalRound(conf_name=CONF_NAME)
    for zone_code in GROUP_CODES[0:4]:
        teams = get_zone_with_teams_of_size(zone_code, CONF_NAME, round_name, team_size=5)
        if teams is not None:
            context[f'zone{zone_code}'] = teams
    context['range'] = GROUP_RANGE
    return render(request, 'asia/finalround.html', context)


def thirdround(request):
    context = {}
    round_name = 'third'
    context['teams'] = getTeamsThirdRound(conf_name=CONF_NAME)

    for zone_code in GROUP_CODES[0:6]:
        teams = get_zone_with_teams_of_size(zone_code, CONF_NAME, round_name)
        if teams is not None:
            context[f'zone{zone_code}'] = teams
    context['range'] = GROUP_RANGE[0:4]
    return render(request, 'asia/thrround.html', context)


def secondround(request):
    context = {}
    round_name = 'second'
    context['teams'] = getTeamsSecondRound(conf_name=CONF_NAME)

    for zone_code in GROUP_CODES[0:6]:
        teams = get_zone_with_teams_of_size(zone_code, CONF_NAME, round_name)
        if teams is not None:
            context[f'zone{zone_code}'] = teams
    context['range'] = GROUP_RANGE[0:4]
    return render(request, 'asia/sndround.html', context)


def firstround(request):
    context = {}
    round_name = 'first'
    context['teams'] = getTeamsFirstRound(conf_name=CONF_NAME)
    for zone_code in GROUP_CODES[0]:
        teams = get_zone_with_teams_of_size(zone_code, CONF_NAME, round_name, team_size=4)
        if teams is not None:
            context[f'zone{zone_code}'] = teams
    context['range'] = GROUP_RANGE[0:4]
    return render(request, 'asia/fstround.html', context)


def teams(request):
    context = {}
    context['teams'] = getTeams(conf_name='AFC')
    return render(request, 'asia/teamlist.html', context)


def updateProgress(request, id, stage):
    if request.method == 'POST':
        updateStage(id, stage)
    return redirect('asia.teams')


def firstRoundButton(request):
    if request.method == 'GET':
        context = {}
        teams_for_match = getTeamsFirstRound(CONF_NAME)
        context['teams'] = teams_for_match
        zones = round_draw(teams_for_match, pools_count=4, teams_per_pool=1)
        for zone_idx, zone in enumerate(zones, start=1):
            random.shuffle(zone)
            create_fixture(zone, False, chr(ord('A') + zone_idx - 1), CONF_NAME, 'first')
            context[f'zone{zone_idx}'] = zone
        return firstround(request)


def secondRoundButton(request):
    if request.method == 'GET':
        context = {}
        teams_for_match = getTeamsSecondRound(CONF_NAME)
        context['teams'] = teams_for_match
        zones = round_draw(teams_for_match, pools_count=4, teams_per_pool=6)
        for zone_idx, zone in enumerate(zones, start=1):
            random.shuffle(zone)
            create_fixture(zone, True, chr(ord('A') + zone_idx - 1), CONF_NAME, 'second')
            context[f'zone{zone_idx}'] = zone

        return secondround(request)

def thirdRoundButton(request):
    if request.method == 'GET':
        context = {}
        teams_for_match = getTeamsThirdRound(CONF_NAME)
        context['teams'] = teams_for_match
        zones = round_draw(teams_for_match, pools_count=4, teams_per_pool=6)
        for zone_idx, zone in enumerate(zones, start=1):
            random.shuffle(zone)
            create_fixture(zone, True, chr(ord('A') + zone_idx - 1), CONF_NAME, 'third')
            context[f'zone{zone_idx}'] = zone
        return thirdround(request)

def finalRoundButton(request):
    if request.method == 'GET':
        context = {}
        teams_for_match = getTeamsFinalRound(CONF_NAME)
        context['teams'] = teams_for_match
        zones = round_draw(teams_for_match, pools_count=5, teams_per_pool=4)
        for zone_idx, zone in enumerate(zones, start=1):
            random.shuffle(zone)
            create_fixture(zone, True, chr(ord('A') + zone_idx - 1), CONF_NAME, 'final')
            context[f'zone{zone_idx}'] = zone

        return finalround(request)