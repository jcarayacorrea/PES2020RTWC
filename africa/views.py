import random

from django.shortcuts import render, redirect

from fixtures import getZoneData, createFixture
from utils import getTeams, updateStage, getTeamsFirstRound, getTeamsSecondRound, getTeamsThirdRound, getTeamsFinalRound


# Create your views here.
def get_zone_teams_qualified(context, zone_name, conf_name, round_name):
    zone_data = getZoneData(zone_name, conf_name, round_name)
    if len(zone_data['teams']) == 5:
        context[f'zone{zone_name}'] = zone_data['teams']


def finalround(request):
    context = {}
    context['teams'] = getTeamsFinalRound(conf_name='CAF')
    zone_names = ['A', 'B', 'C', 'D', 'E']
    for zone in zone_names:
        get_zone_teams_qualified(context, zone, 'CAF', 'final')
    context['range'] = ['1','2','3','4','5']
    return render(request, 'africa/finalround.html', context)


def thirdround(request):
    context = {}
    context['teams'] = getTeamsThirdRound(conf_name='CAF')

    def set_zone_context(zone_index):
        zone_data = getZoneData(zone_index, 'CAF', 'third')
        if len(zone_data['teams']) == 4:
            context['zone' + zone_index] = zone_data['teams']

    for zone_index in ['A', 'B', 'C', 'D', 'E']:
        set_zone_context(zone_index)
    context['range'] = ['1', '2', '3', '4', '5']
    return render(request, 'africa/thrround.html', context)


def secondround(request):
    def process_zone(zone_id):
        zone_data = getZoneData(zone_id, 'CAF', 'second')
        if len(zone_data['teams']) == 4:
            return zone_data['teams']
        return None

    context = {'teams': getTeamsSecondRound(conf_name='CAF')}

    for i in range(1, 6):
        zone = process_zone(chr(64 + i))  # chr(65) = 'A', chr(66) = 'B', ..
        if zone is not None:
            context[f'zone{i}'] = zone
    context['range'] = ['1', '2', '3', '4', '5']
    return render(request, 'africa/sndround.html', context)


def add_zone_to_context_if_full(zone_name, zone_data, context):
    if len(zone_data['teams']) == 4:
        context[zone_name] = zone_data['teams']
    return context


def firstround(request):
    context = {}
    context['teams'] = getTeamsFirstRound(conf_name='CAF')
    zones = ['A', 'B', 'C']
    for i in range(3):
        zone_data = getZoneData(zones[i], 'CAF', 'first')
        context = add_zone_to_context_if_full('zone' + str(i + 1), zone_data, context)
    context['range'] = ['1', '2', '3']
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
        CONF_NAME = 'CAF'

        def shuffle_and_create_fixture(zone, zone_letter):
            random.shuffle(zone)
            createFixture(zone, False, zone_letter, CONF_NAME, 'first')
            return zone

        context = {'teams': getTeamsFirstRound(CONF_NAME)}
        zone1, zone2, zone3 = firstRoundDraw(getTeamsFirstRound(CONF_NAME))
        context['zone1'] = shuffle_and_create_fixture(zone1, 'A')
        context['zone2'] = shuffle_and_create_fixture(zone2, 'B')
        context['zone3'] = shuffle_and_create_fixture(zone3, 'C')
        return firstround(request)


import random


def shuffle_pool(teams, pool_size):
    pool = [teams[i:i + pool_size] for i in range(0, len(teams), pool_size)]
    random.shuffle(pool)
    return pool


def firstRoundDraw(teams):
    pool_size = 3
    pools = shuffle_pool(teams, pool_size)

    def create_zones(pools, pool_size):
        return [[pools[j][i] for j in range(len(pools))] for i in range(pool_size)]

    zones = create_zones(pools, pool_size)

    return zones


def secondRoundButton(request):
    if request.method == 'GET':
        context = {}
        zone_names = ['A', 'B', 'C', 'D', 'E']
        teams_second_round = getTeamsSecondRound('CAF')
        zones = list(secondRoundDraw(teams_second_round))
        context['teams'] = teams_second_round

        for i in range(len(zones)):
            random.shuffle(zones[i])
            createFixture(zones[i], True, zone_names[i], 'CAF', 'second')
            context[f'zone{i + 1}'] = zones[i]

        return secondround(request, context)


import random


def secondRoundDraw(teams):
    pools = [teams[i:i + 5] for i in range(0, len(teams), 5)]
    [random.shuffle(pool) for pool in pools]
    zones = [[pool[j] for pool in pools] for j in range(5)]
    return zones


def shuffle_and_create_fixture(zone, group_char, confederation, round):
    random.shuffle(zone)
    createFixture(zone, True, group_char, confederation, round)
    return zone


def thirdRoundButton(request):
    CONFEDERATION = 'CAF'
    ROUND = 'third'

    if request.method == 'GET':
        context = {}
        teams = getTeamsThirdRound(CONFEDERATION)
        zone1, zone2, zone3, zone4, zone5 = thirdRoundDraw(teams)
        context['zone1'] = shuffle_and_create_fixture(zone1, 'A', CONFEDERATION, ROUND)
        context['zone2'] = shuffle_and_create_fixture(zone2, 'B', CONFEDERATION, ROUND)
        context['zone3'] = shuffle_and_create_fixture(zone3, 'C', CONFEDERATION, ROUND)
        context['zone4'] = shuffle_and_create_fixture(zone4, 'D', CONFEDERATION, ROUND)
        context['zone5'] = shuffle_and_create_fixture(zone5, 'E', CONFEDERATION, ROUND)

        return thirdround(request)


import random

NUMBER_OF_TEAMS_IN_POOLS = 5
NUMBER_OF_POOLS = 4


def shuffle_teams(teams):
    random.shuffle(teams)
    return teams


def thirdRoundDraw(teams):
    pools = [shuffle_teams(teams[i:i + NUMBER_OF_TEAMS_IN_POOLS])
             for i in range(0, NUMBER_OF_TEAMS_IN_POOLS * NUMBER_OF_POOLS, NUMBER_OF_TEAMS_IN_POOLS)]

    zones = [[pool[i] for pool in pools] for i in range(NUMBER_OF_TEAMS_IN_POOLS)]

    return zones


def shuffle_teams_and_create_fixture(zone, zone_name, context, conf='CAF', round_='final'):
    random.shuffle(zone)
    createFixture(zone, True, zone_name, conf, round_)
    context[zone_name.lower()] = zone


def finalRoundButton(request):
    if request.method == 'GET':
        context = {}
        conf = 'CAF'
        context['teams'] = getTeamsFinalRound(conf)
        zones = finalRoundDraw(getTeamsFinalRound(conf))
        for i, zone in enumerate(zones, 1):
            shuffle_teams_and_create_fixture(zone, f'zone{i}', context)
        return finalround(request)


def drawAndShuffleTeams(teams, start, end):
    pool = teams[start:end]
    random.shuffle(pool)
    return pool


def finalRoundDraw(teams):
    pools = [drawAndShuffleTeams(teams, i, i + 5) for i in range(0, 25, 5)]
    zones = [[pools[j][i] for j in range(5)] for i in range(5)]
    return tuple(zones)
