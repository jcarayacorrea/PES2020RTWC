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


def firstRoundDraw(teams):
    pool1 = [teams[0], teams[1]]
    pool2 = [teams[2], teams[3]]
    pool3 = [teams[4], teams[5]]
    pool4 = [teams[6], teams[7]]
    pool5 = [teams[8], teams[9]]

    random.shuffle(pool1)
    random.shuffle(pool2)
    random.shuffle(pool3)
    random.shuffle(pool4)
    random.shuffle(pool5)

    zone1 = [pool1[0], pool2[0], pool3[0], pool4[0], pool5[0]]
    zone2 = [pool1[1], pool2[1], pool3[1], pool4[1], pool5[1]]

    return zone1, zone2


def secondRoundButton(request):
    if request.method == 'GET':
        context = {}
        context['teams'] = getTeamsSecondRound('UEFA')
        zone1, zone2, zone3, zone4, zone5, zone6 = secondRoundDraw(getTeamsSecondRound('UEFA'))
        random.shuffle(zone1)
        random.shuffle(zone2)
        random.shuffle(zone3)
        random.shuffle(zone4)
        random.shuffle(zone5)
        random.shuffle(zone6)
        createFixture(zone1, True, 'A', 'UEFA', 'second')
        createFixture(zone2, True, 'B', 'UEFA', 'second')
        createFixture(zone3, True, 'C', 'UEFA', 'second')
        createFixture(zone4, True, 'D', 'UEFA', 'second')
        createFixture(zone5, True, 'E', 'UEFA', 'second')
        createFixture(zone6, True, 'F', 'UEFA', 'second')

        context['zone1'] = zone1
        context['zone2'] = zone2
        context['zone3'] = zone3
        context['zone4'] = zone4
        context['zone5'] = zone5
        context['zone6'] = zone6

        return secondround(request)


def secondRoundDraw(teams):
    pool1 = [teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]]
    pool2 = [teams[6], teams[7], teams[8], teams[9], teams[10], teams[11]]
    pool3 = [teams[12], teams[13], teams[14], teams[15], teams[16], teams[17]]
    pool4 = [teams[18], teams[19], teams[20], teams[21], teams[22], teams[23]]

    random.shuffle(pool1)
    random.shuffle(pool2)
    random.shuffle(pool3)
    random.shuffle(pool4)

    zone1 = [pool1[0], pool2[0], pool3[0], pool4[0]]
    zone2 = [pool1[1], pool2[1], pool3[1], pool4[1]]
    zone3 = [pool1[2], pool2[2], pool3[2], pool4[2]]
    zone4 = [pool1[3], pool2[3], pool3[3], pool4[3]]
    zone5 = [pool1[4], pool2[4], pool3[4], pool4[4]]
    zone6 = [pool1[5], pool2[5], pool3[5], pool4[5]]

    return zone1, zone2, zone3, zone4, zone5, zone6


def thirdRoundButton(request):
    if request.method == 'GET':
        context = {}
        context['teams'] = getTeamsThirdRound('UEFA')
        zone1, zone2, zone3, zone4, zone5, zone6, zone7, zone8 = thirdRoundDraw(getTeamsThirdRound('UEFA'))
        random.shuffle(zone1)
        random.shuffle(zone2)
        random.shuffle(zone3)
        random.shuffle(zone4)
        random.shuffle(zone5)
        random.shuffle(zone6)
        random.shuffle(zone7)
        random.shuffle(zone8)

        createFixture(zone1, True, 'A', 'UEFA', 'third')
        createFixture(zone2, True, 'B', 'UEFA', 'third')
        createFixture(zone3, True, 'C', 'UEFA', 'third')
        createFixture(zone4, True, 'D', 'UEFA', 'third')
        createFixture(zone5, True, 'E', 'UEFA', 'third')
        createFixture(zone6, True, 'F', 'UEFA', 'third')
        createFixture(zone7, True, 'G', 'UEFA', 'third')
        createFixture(zone8, True, 'H', 'UEFA', 'third')

        context['zone1'] = zone1
        context['zone2'] = zone2
        context['zone3'] = zone3
        context['zone4'] = zone4
        context['zone5'] = zone5
        context['zone6'] = zone6
        context['zone7'] = zone7
        context['zone8'] = zone8

        return thirdround(request)


def thirdRoundDraw(teams):
    pool1 = [teams[0], teams[1], teams[2], teams[3], teams[4], teams[5], teams[6], teams[7]]
    pool2 = [teams[8], teams[9], teams[10], teams[11], teams[12], teams[13], teams[14], teams[15]]
    pool3 = [teams[16], teams[17], teams[18], teams[19], teams[20], teams[21], teams[22], teams[23]]

    random.shuffle(pool1)
    random.shuffle(pool2)
    random.shuffle(pool3)

    zone1 = [pool1[0], pool2[0], pool3[0]]
    zone2 = [pool1[1], pool2[1], pool3[1]]
    zone3 = [pool1[2], pool2[2], pool3[2]]
    zone4 = [pool1[3], pool2[3], pool3[3]]
    zone5 = [pool1[4], pool2[4], pool3[4]]
    zone6 = [pool1[5], pool2[5], pool3[5]]
    zone7 = [pool1[6], pool2[6], pool3[6]]
    zone8 = [pool1[7], pool2[7], pool3[7]]

    return zone1, zone2, zone3, zone4, zone5, zone6, zone7, zone8


def finalRoundButton(request):
    if request.method == 'GET':
        context = {}
        context['teams'] = getTeamsFinalRound('UEFA')
        zone1, zone2, zone3, zone4 = finalRoundDraw(getTeamsFinalRound('UEFA'))
        random.shuffle(zone1)
        random.shuffle(zone2)
        random.shuffle(zone3)
        random.shuffle(zone4)

        createFixture(zone1, True, 'A', 'UEFA', 'final')
        createFixture(zone2, True, 'B', 'UEFA', 'final')
        createFixture(zone3, True, 'C', 'UEFA', 'final')
        createFixture(zone4, True, 'D', 'UEFA', 'final')

        context['zone1'] = zone1
        context['zone2'] = zone2
        context['zone3'] = zone3
        context['zone4'] = zone4

        return finalround(request)


def finalRoundDraw(teams):
    pool1 = [teams[0], teams[1], teams[2], teams[3]]
    pool2 = [teams[4], teams[5], teams[6], teams[7]]
    pool3 = [teams[8], teams[9], teams[10], teams[11]]
    pool4 = [teams[12], teams[13], teams[14], teams[15]]
    pool5 = [teams[16], teams[17], teams[18], teams[19]]

    random.shuffle(pool1)
    random.shuffle(pool2)
    random.shuffle(pool3)
    random.shuffle(pool4)
    random.shuffle(pool5)

    zone1 = [pool1[0], pool2[0], pool3[0], pool4[0], pool5[0]]
    zone2 = [pool1[1], pool2[1], pool3[1], pool4[1], pool5[1]]
    zone3 = [pool1[2], pool2[2], pool3[2], pool4[2], pool5[2]]
    zone4 = [pool1[3], pool2[3], pool3[3], pool4[3], pool5[3]]

    return zone1, zone2, zone3, zone4


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
