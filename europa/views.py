import random

from django.shortcuts import render, redirect

from Global_Variables import GROUP_KEYS, GROUP_RANGE
from draw import round_draw, get_zone_with_teams_of_size
from fixtures import getZoneData, create_fixture
from utils import getTeams, updateStage, getTeamsFinalRound, getTeamsThirdRound, getTeamsSecondRound, \
    getTeamsFirstRound, db_conexion, getTeamById

CONF_NAME = 'UEFA'


# Create your views here.

def finalround(request):
    context = {}
    round_name = 'final'
    context['teams'] = getTeamsFinalRound(conf_name=CONF_NAME)
    for zone_code in GROUP_KEYS[0:4]:
        teams = get_zone_with_teams_of_size(zone_code, CONF_NAME, round_name, team_size=5)
        if teams is not None:
            context[f'zone{zone_code}'] = teams
    context['range'] = GROUP_RANGE
    return render(request, 'europa/finalround.html', context)


def thirdround(request):
    context = {}
    round_name = 'third'
    context['teams'] = getTeamsThirdRound(conf_name=CONF_NAME)

    for zone_code in GROUP_KEYS:
        teams = get_zone_with_teams_of_size(zone_code, CONF_NAME, round_name, team_size=3)
        if teams is not None:
            context[f'zone{zone_code}'] = teams
    context['range'] = GROUP_RANGE[0:3]
    return render(request, 'europa/thrround.html', context)


def secondround(request):
    context = {}
    round_name = 'second'
    context['teams'] = getTeamsSecondRound(conf_name=CONF_NAME)

    for zone_code in GROUP_KEYS[0:6]:
        teams = get_zone_with_teams_of_size(zone_code, CONF_NAME, round_name)
        if teams is not None:
            context[f'zone{zone_code}'] = teams
    context['range'] = GROUP_RANGE[0:4]
    return render(request, 'europa/sndround.html', context)


def firstround(request):
    context = {}
    round_name = 'first'
    context['teams'] = getTeamsFirstRound(conf_name=CONF_NAME)
    for zone_code in GROUP_KEYS[0:2]:
        teams = get_zone_with_teams_of_size(zone_code, CONF_NAME, round_name, team_size=5)
        if teams is not None:
            context[f'zone{zone_code}'] = teams
    fixture = getZoneData('WC', 'UEFA', 'first')
    context['fixture'] = fixture['fixtures']
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
        zones = round_draw(teams_for_match, pools_count=5, teams_per_pool=2)
        for zone_idx, zone in enumerate(zones, start=1):
            random.shuffle(zone)
            create_fixture(zone, False, chr(ord('A') + zone_idx - 1), 'UEFA', 'first')
            context[f'zone{zone_idx}'] = zone
        return firstround(request)


def secondRoundButton(request):
    if request.method == 'GET':
        context = {}
        teams_for_match = getTeamsSecondRound('UEFA')
        context['teams'] = teams_for_match
        zones = round_draw(teams_for_match, pools_count=4, teams_per_pool=6)
        for zone_idx, zone in enumerate(zones, start=1):
            random.shuffle(zone)
            create_fixture(zone, True, chr(ord('A') + zone_idx - 1), 'UEFA', 'second')
            context[f'zone{zone_idx}'] = zone
        return secondround(request)


def thirdRoundButton(request):
    if request.method == 'GET':
        context = {}
        teams_for_match = getTeamsThirdRound('UEFA')
        context['teams'] = teams_for_match
        zones = round_draw(teams_for_match, pools_count=3, teams_per_pool=8)
        for zone_idx, zone in enumerate(zones, start=1):
            random.shuffle(zone)
            create_fixture(zone, True, chr(ord('A') + zone_idx - 1), 'UEFA', 'third')
            context[f'zone{zone_idx}'] = zone
        return thirdround(request)


def finalRoundButton(request):
    if request.method == 'GET':
        context = {}
        teams_for_match = getTeamsFinalRound('UEFA')
        context['teams'] = teams_for_match
        zones = round_draw(teams_for_match, pools_count=5, teams_per_pool=4)
        for zone_idx, zone in enumerate(zones, start=1):
            random.shuffle(zone)
            create_fixture(zone, True, chr(ord('A') + zone_idx - 1), 'UEFA', 'final')
            context[f'zone{zone_idx}'] = zone
        return finalround(request)


def setHomeWildCardTeam(request):
    db = db_conexion()
    teamId = request.GET.get('team')
    team = getTeamById(teamId)
    db.get_collection('Fixtures').update_many({'$and': [{'conf': 'UEFA'}, {'zone': 'WC'}, {'round': 'first'}]},
                                              {'$set': {
                                                  'fixtures.wildCard.match1.played': False,
                                                  'fixtures.wildCard.match1.homeTeam.team': team[0],
                                                  'fixtures.wildCard.match1.homeTeam.goals': None,
                                                  'fixtures.wildCard.match1.homeTeam.penalties': None
                                              }})
    return firstround(request)


def setAwayWildCardTeam(request):
    db = db_conexion()
    teamId = request.GET.get('team')
    team = getTeamById(teamId)
    db.get_collection('Fixtures').update_one({'$and': [{'conf': 'UEFA'}, {'zone': 'WC'}, {'round': 'first'}]},
                                             {'$set': {
                                                 'fixtures.wildCard.match1.played': False,
                                                 'fixtures.wildCard.match1.awayTeam.team': team[0],
                                                 'fixtures.wildCard.match1.awayTeam.goals': None,
                                                 'fixtures.wildCard.match1.awayTeam.penalties': None
                                             }})
    return firstround(request)
