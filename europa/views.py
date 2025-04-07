import random

from django.shortcuts import render, redirect

from fixtures import getZoneData, createFixture
from utils import getTeams, updateStage, getTeamsFinalRound, getTeamsThirdRound, getTeamsSecondRound, \
    getTeamsFirstRound, db_conexion, getTeamById


# Create your views here.

def get_valid_zone_data(zone_name):
    zone_data = getZoneData(zone_name, 'UEFA', 'final')
    if len(zone_data['teams']) == 5:
        return zone_data['teams']
    else:
        return None


def finalround(request):
    context = {}
    context['teams'] = getTeamsFinalRound(conf_name='UEFA')
    for zone in ['A', 'B', 'C', 'D']:
        zone_teams = get_valid_zone_data(zone)
        if zone_teams is not None:
            context[f'zone{zone}'] = zone_teams
    context['range'] = ['1', '2', '3', '4','5']
    return render(request, 'europa/finalround.html', context)





def _assign_teams_if_enough(context, zone_id, conf_name, round_number):
    zone_data = getZoneData(zone_id, conf_name, round_number)
    if len(zone_data['teams']) == 3:
        context[f'zone{zone_id}'] = zone_data['teams']
    return context


def thirdround(request):
    context = {}
    context['teams'] = getTeamsThirdRound(conf_name='UEFA')

    for zone_id in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
        context = _assign_teams_if_enough(context, zone_id, 'UEFA', 'third')
    context['range'] = ['1', '2', '3']
    return render(request, 'europa/thrround.html', context)


def get_zone_with_teams_of_size(zone_code, conf_name, round_name, team_size=4):
    zone_data = getZoneData(zone_code, conf_name, round_name)
    if len(zone_data['teams']) == team_size:
        return zone_data['teams']
    return None


def secondround(request):
    context = {}
    conf_name = 'UEFA'
    round_name = 'second'

    context['teams'] = getTeamsSecondRound(conf_name=conf_name)

    for zone_code in ['A', 'B', 'C', 'D', 'E', 'F']:
        teams = get_zone_with_teams_of_size(zone_code, conf_name, round_name)
        if teams is not None:
            context[f'zone{zone_code}'] = teams
    context['range'] = ['1', '2', '3', '4']
    return render(request, 'europa/sndround.html', context)


def firstround(request):
    def get_team_data_for_zone(zone, round):
        zone_data = getZoneData(zone, 'UEFA', round)
        return zone_data['teams'] if len(zone_data['teams']) == 5 else None

    context = {
        'teams': getTeamsFirstRound('UEFA'),
        'zone1': get_team_data_for_zone('A', 'first'),
        'zone2': get_team_data_for_zone('B', 'first'),
        'fixture': getZoneData('WC', 'UEFA', 'first')['fixtures'],
        'range': ['1', '2', '3', '4','5']
    }
    return render(request, 'europa/fstround.html', context)


def teams(request):
    context = {}
    context['teams'] = getTeams(conf_name='UEFA')
    return render(request, 'europa/teamlist.html', context)


def updateProgress(request, id, stage):
    if request.method == 'POST':
        updateStage(id, stage)
    return redirect('europa.teams')


def prepareFirstRoundMatch(request):
    if request.method == 'GET':
        context = {}
        teams_for_match = getTeamsFirstRound('UEFA')
        context['teams'] = teams_for_match
        zones = firstRoundDraw(teams_for_match)
        for zone_idx, zone in enumerate(zones, start=1):
            random.shuffle(zone)
            createFixture(zone, False, chr(ord('A') + zone_idx - 1), 'UEFA', 'first')
            context[f'zone{zone_idx}'] = zone
        return firstround(request)


def shuffle_and_pick(teams, pick_size):
    random.shuffle(teams)
    return [teams[i] for i in range(pick_size)]


def firstRoundDraw(teams, pools_count=5, teams_per_pool=2):
    zones = [[] for _ in range(teams_per_pool)]
    for p in range(pools_count):
        pool = shuffle_and_pick(teams[p * teams_per_pool:(p + 1) * teams_per_pool], teams_per_pool)
        for idx, team in enumerate(pool):
            zones[idx].append(team)
    return zones


def shuffle_zones_and_create_fixtures(zones: list, round_name: str, conf_name: str):
    for idx, zone in enumerate(zones):
        random.shuffle(zone)
        createFixture(zone, True, chr(65 + idx), conf_name, round_name)


def build_context(context: dict, zones: list):
    for idx, zone in enumerate(zones):
        context[f'zone{idx + 1}'] = zone


def secondRoundButton(request):
    if request.method == 'GET':
        context = {}
        teams = getTeamsSecondRound('UEFA')
        context['teams'] = teams
        zones = secondRoundDraw(teams)
        shuffle_zones_and_create_fixtures(zones, 'second', 'UEFA')
        build_context(context, zones)
        return secondround(request)


def secondRoundDraw(teams):
    pool_size = 6
    num_pools = 4
    pools = [teams[i:i + pool_size] for i in range(0, len(teams), pool_size)]
    for pool in pools:
        random.shuffle(pool)

    zones = [[pools[j][i] for j in range(num_pools)] for i in range(pool_size)]
    return zones


def process_zone(zone, group_name, conf_name, round_name):
    random.shuffle(zone)
    createFixture(zone, True, group_name, conf_name, round_name)
    return zone


def thirdRoundButton(request):
    if request.method == 'GET':
        context = {}
        all_teams = getTeamsThirdRound('UEFA')
        context['teams'] = all_teams
        zones = thirdRoundDraw(all_teams)
        group_names = list('ABCDEFGH')

        for i in range(8):
            zone_name = f'zone{i + 1}'
            context[zone_name] = process_zone(zones[i], group_names[i], 'UEFA', 'third')

        return thirdround(request)


def thirdRoundDraw(teams):
    pools = [teams[n * 8:(n + 1) * 8] for n in range(3)]
    for pool in pools:
        random.shuffle(pool)
    zones = [[pool[i] for pool in pools] for i in range(8)]
    return tuple(zones)


CONF_NAME = 'UEFA'
ROUND_NAME = 'final'


def shuffle_and_create_fixture(zone, zone_name):
    random.shuffle(zone)
    createFixture(zone, True, zone_name, CONF_NAME, ROUND_NAME)


def finalRoundButton(request):
    if request.method == 'GET':
        context = {}
        teams = getTeamsFinalRound(CONF_NAME)
        context['teams'] = teams
        zones = finalRoundDraw(teams)
        zone_names = ['A', 'B', 'C', 'D']

        for i in range(4):
            shuffle_and_create_fixture(zones[i], zone_names[i])
            context[f'zone{i + 1}'] = zones[i]

        return finalround(request)


import random


def finalRoundDraw(teams):
    pools = [random.shuffle(teams[i:i + 4]) for i in range(0, len(teams), 4)]

    zones = []
    for i in range(4):
        zones.append([pool[i] for pool in pools])

    return zones


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
