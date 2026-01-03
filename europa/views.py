import random

from django.shortcuts import render, redirect

from Global_Variables import GROUP_KEYS, GROUP_RANGE
from draw import round_draw, get_zone_with_teams_of_size
from fixtures import getZoneData, create_fixture, createPlayOffMatches, createPlayOffMatchesUEFA
from utils import getTeams, updateStage, getTeamsFinalRound, getUEFATeamsPlayoff, \
    getTeamsFirstRound, db_conexion, getTeamById

CONF_NAME = 'UEFA'


# Create your views here.

def finalround(request):
    context = {}
    round_name = 'final'
    context['teams'] = getTeamsFinalRound(conf_name=CONF_NAME)
    for zone_code in GROUP_KEYS:
        teams = get_zone_with_teams_of_size(zone_code, CONF_NAME, round_name, team_size=5)
        if teams is not None:
            context[f'zone{zone_code}'] = teams
    context['range'] = GROUP_RANGE
    return render(request, 'europa/finalround.html', context)



def firstround(request):
    context = {}
    round_name = 'first'
    context['teams'] = getTeamsFirstRound(conf_name=CONF_NAME)
    for zone_code in GROUP_KEYS[0:5]:
        teams = get_zone_with_teams_of_size(zone_code, CONF_NAME, round_name, team_size=5)
        if teams is not None:
            context[f'zone{zone_code}'] = teams
    context['range'] = GROUP_RANGE
    return render(request, 'europa/fstround.html', context)


def teams(request):
    context = {}
    context['teams'] = getTeams(conf_name='UEFA')
    return render(request, 'europa/teamlist.html', context)


def updateProgress(request, code, stage):
    if request.method == 'POST':
        updateStage(code, stage)
    return redirect('europa.teams')


def firstRoundButton(request):
    if request.method == 'GET':
        context = {}
        teams_for_match = getTeamsFirstRound('UEFA')
        context['teams'] = teams_for_match
        zones = round_draw(teams_for_match, pools_count=5, teams_per_pool=5)
        for zone_idx, zone in enumerate(zones, start=1):
            random.shuffle(zone)
            create_fixture(zone, True, chr(ord('A') + zone_idx - 1), 'UEFA', 'first')
            context[f'zone{zone_idx}'] = zone
        return firstround(request)


def finalRoundButton(request):
    if request.method == 'GET':
        context = {}
        teams_for_match = getTeamsFinalRound('UEFA')
        context['teams'] = teams_for_match
        zones = round_draw(teams_for_match, pools_count=5, teams_per_pool=8)
        for zone_idx, zone in enumerate(zones, start=1):
            random.shuffle(zone)
            create_fixture(zone, True, chr(ord('A') + zone_idx - 1), 'UEFA', 'final')
            context[f'zone{zone_idx}'] = zone
        return finalround(request)


def euroPlayoff(request):
    context = getPlayOffContextData()
    return render(request, 'europa/playoff.html', context)

def getPlayoffPage(request):
    if request.method == 'GET':
        playoffTeams, playoffFixtures = preparePlayoffData()
        context = {'teams': playoffTeams, 'fixture': playoffFixtures}
        return render(request, 'europa/playoff.html', context)

def getPlayOffContextData():
    context = {}
    context['teams'] = getUEFATeamsPlayoff('UEFA')
    playoffData = getZoneData('P', 'UEFA', 'playoff')
    context['fixture'] = playoffData['fixtures']
    return context

def playoffDraw(teams):
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

def preparePlayoffData():
    teams = getUEFATeamsPlayoff('UEFA')
    zones = playoffDraw(teams)
    for zone in zones:
        random.shuffle(zone)
    createPlayOffMatchesUEFA(teams, *zones)
    zone_identifier = 'P'
    round_type = 'playoff'
    playoffData = getZoneData(zone_identifier, CONF_NAME, round_type)

    return teams, playoffData['fixtures']


