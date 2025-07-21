import random

from django.shortcuts import render, redirect

from Global_Variables import GROUP_RANGE, GROUP_KEYS
from draw import get_zone_with_teams_of_size, round_draw
from fixtures import getZoneData, create_fixture
from utils import updateStage, getTeams, getTeamsFirstRound, getTeamsFinalRound, db_conexion, getTeamById


CONF_NAME = 'OFC'


# Create your views here.
def finalround(request):
    context = {}
    round_name = 'final'
    context['teams'] = getTeamsFinalRound(conf_name=CONF_NAME)
    for zone_code in GROUP_KEYS[0:2]:
        teams = get_zone_with_teams_of_size(zone_code, CONF_NAME, round_name, team_size=4)
        if teams is not None:
            context[f'zone{zone_code}'] = teams
    fixture = getZoneData('MD', 'OFC', 'final')
    context['fixture'] = fixture['fixtures']
    context['range'] = GROUP_RANGE[0:4]

    return render(request, 'oceania/finalround.html', context)


def firstround(request):
    context = {}
    round_name = 'first'
    context['teams'] = getTeamsFirstRound(conf_name=CONF_NAME)
    for zone_code in GROUP_KEYS[0]:
        teams = get_zone_with_teams_of_size(zone_code, CONF_NAME, round_name, team_size=5)
        if teams is not None:
            context[f'zone{zone_code}'] = teams
    context['range'] = GROUP_RANGE
    return render(request, 'oceania/fstround.html', context)


def teams(request):
    context = {}
    context['teams'] = getTeams(conf_name='OFC')
    return render(request, 'oceania/teamlist.html', context)


def updateProgress(request, code, stage):
    if request.method == 'POST':
        updateStage(code, stage)
    return redirect('oceania.teams')


def firstRoundButton(request):
    if request.method == 'GET':
        context = {}
        teams_for_match = getTeamsFirstRound(CONF_NAME)
        context['teams'] = teams_for_match
        zones = round_draw(teams_for_match, pools_count=5, teams_per_pool=1)
        for zone_idx, zone in enumerate(zones, start=1):
            random.shuffle(zone)
            create_fixture(zone, False, chr(ord('A') + zone_idx - 1), CONF_NAME, 'first')
            context[f'zone{zone_idx}'] = zone
        return firstround(request)


def finalRoundButton(request):
    if request.method == 'GET':
        context = {}
        teams_for_match = getTeamsFinalRound(CONF_NAME)
        context['teams'] = teams_for_match
        zones = round_draw(teams_for_match, pools_count=4, teams_per_pool=2)
        for zone_idx, zone in enumerate(zones, start=1):
            random.shuffle(zone)
            create_fixture(zone, True, chr(ord('A') + zone_idx - 1), CONF_NAME, 'final')
            context[f'zone{zone_idx}'] = zone
        return finalround(request)


def setHomeFinalTeam(request):
    db = db_conexion()
    teamId = request.GET.get('team')
    team = getTeamById(teamId)
    db.get_collection('Fixtures').update_many({'$and': [{'conf': 'OFC'}, {'zone': 'MD'}, {'round': 'final'}]},
                                              {'$set': {
                                                  'fixtures.mainDraw.match1.played': False,
                                                  'fixtures.mainDraw.match1.homeTeam.team': team[0],
                                                  'fixtures.mainDraw.match1.homeTeam.goals': None,
                                                  'fixtures.mainDraw.match1.homeTeam.penalties': None
                                              }})
    return finalround(request)


def setAwayFinalTeam(request):
    db = db_conexion()
    teamId = request.GET.get('team')
    team = getTeamById(teamId)
    db.get_collection('Fixtures').update_one({'$and': [{'conf': 'OFC'}, {'zone': 'MD'}, {'round': 'final'}]},
                                             {'$set': {
                                                 'fixtures.mainDraw.match1.played': False,
                                                 'fixtures.mainDraw.match1.awayTeam.team': team[0],
                                                 'fixtures.mainDraw.match1.awayTeam.goals': None,
                                                 'fixtures.mainDraw.match1.awayTeam.penalties': None
                                             }})
    return finalround(request)
