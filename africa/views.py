import random

from django.shortcuts import render, redirect

from Global_Variables import GROUP_KEYS, GROUP_RANGE
from fixtures import getZoneData, create_fixture
from utils import getTeams, updateStage, getTeamsFirstRound, getTeamsSecondRound, getTeamsThirdRound, \
    getTeamsFinalRound
from draw import round_draw, get_zone_with_teams_of_size

CONF_NAME = 'CAF'


# Create your views here.

def finalround(request):
    context = {}
    round_name = 'final'
    context['teams'] = getTeamsFinalRound(conf_name=CONF_NAME)
    for zone_code in GROUP_KEYS[0:5]:
        teams = get_zone_with_teams_of_size(zone_code, CONF_NAME, round_name, team_size=5)
        if teams is not None:
            context[f'zone{zone_code}'] = teams
    context['range'] = GROUP_RANGE
    return render(request, 'africa/finalround.html', context)


def thirdround(request):
    context = {}
    round_name = 'third'
    context['teams'] = getTeamsThirdRound(conf_name=CONF_NAME)
    for zone_code in GROUP_KEYS[0:5]:
        teams = get_zone_with_teams_of_size(zone_code, CONF_NAME, round_name, team_size=4)
        if teams is not None:
            context[f'zone{zone_code}'] = teams
    context['range'] = GROUP_RANGE[0:4]
    return render(request, 'africa/thrround.html', context)


def secondround(request):
    context = {}
    round_name = 'second'
    context['teams'] = getTeamsSecondRound(conf_name=CONF_NAME)
    for zone_code in GROUP_KEYS[0:5]:
        teams = get_zone_with_teams_of_size(zone_code, CONF_NAME, round_name, team_size=4)
        if teams is not None:
            context[f'zone{zone_code}'] = teams
    context['range'] = GROUP_RANGE[0:4]
    return render(request, 'africa/sndround.html', context)


def firstround(request):
    context = {}
    round_name = 'first'
    context['teams'] = getTeamsFirstRound(conf_name=CONF_NAME)
    for zone_code in GROUP_KEYS[0:3]:
        teams = get_zone_with_teams_of_size(zone_code, CONF_NAME, round_name, team_size=4)
        if teams is not None:
            context[f'zone{zone_code}'] = teams
    context['range'] = GROUP_RANGE[0:4]
    return render(request, 'africa/fstround.html', context)


def teams(request):
    context = {}
    context['teams'] = getTeams(conf_name='CAF')
    return render(request, 'africa/teamlist.html', context)


def updateProgress(request, id, stage):
    if request.method == 'POST':
        updateStage(id, stage)
    return redirect('africa.teams')


def firstRoundButton(request):
    if request.method == 'GET':
        context = {}
        teams_for_match = getTeamsFirstRound(CONF_NAME)
        context['teams'] = teams_for_match
        zones = round_draw(teams_for_match, pools_count=4, teams_per_pool=3)
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
        zones = round_draw(teams_for_match, pools_count=4, teams_per_pool=5)
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
        zones = round_draw(teams_for_match, pools_count=4, teams_per_pool=5)
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
        zones = round_draw(teams_for_match, pools_count=5, teams_per_pool=5)
        for zone_idx, zone in enumerate(zones, start=1):
            random.shuffle(zone)
            create_fixture(zone, True, chr(ord('A') + zone_idx - 1), CONF_NAME, 'final')
            context[f'zone{zone_idx}'] = zone
        return finalround(request)
