import random

from django.shortcuts import render, redirect

from fixtures import getZoneData, createFixture
from utils import getTeams, updateStage, getTeamsFinalRound, getTeamsThirdRound, getTeamsSecondRound, \
    getTeamsFirstRound, db_conexion, getTeamById


# Create your views here.

def finalround(request):
    context = {}
    context['teams'] = getTeamsFinalRound(conf_name='UEFA')
    zone1 = getZoneData('A', 'UEFA', 'final')
    zone2 = getZoneData('B', 'UEFA', 'final')
    zone3 = getZoneData('C', 'UEFA', 'final')
    zone4 = getZoneData('D', 'UEFA', 'final')
    if len(zone1['teams']) == 5:
        context['zone1'] = zone1['teams']
    if len(zone2['teams']) == 5:
        context['zone2'] = zone2['teams']
    if len(zone3['teams']) == 5:
        context['zone3'] = zone3['teams']
    if len(zone4['teams']) == 5:
        context['zone4'] = zone4['teams']
    return render(request, 'europa/finalround.html', context)


def thirdround(request):
    context = {}
    context['teams'] = getTeamsThirdRound(conf_name='UEFA')
    zone1 = getZoneData('A', 'UEFA', 'third')
    zone2 = getZoneData('B', 'UEFA', 'third')
    zone3 = getZoneData('C', 'UEFA', 'third')
    zone4 = getZoneData('D', 'UEFA', 'third')
    zone5 = getZoneData('E', 'UEFA', 'third')
    zone6 = getZoneData('F', 'UEFA', 'third')
    zone7 = getZoneData('G', 'UEFA', 'third')
    zone8 = getZoneData('H', 'UEFA', 'third')

    if len(zone1['teams']) == 3:
        context['zone1'] = zone1['teams']
    if len(zone2['teams']) == 3:
        context['zone2'] = zone2['teams']
    if len(zone3['teams']) == 3:
        context['zone3'] = zone3['teams']
    if len(zone4['teams']) == 3:
        context['zone4'] = zone4['teams']
    if len(zone5['teams']) == 3:
        context['zone5'] = zone5['teams']
    if len(zone6['teams']) == 3:
        context['zone6'] = zone6['teams']
    if len(zone7['teams']) == 3:
        context['zone7'] = zone7['teams']
    if len(zone8['teams']) == 3:
        context['zone8'] = zone8['teams']
    return render(request, 'europa/thrround.html', context)


def secondround(request):
    context = {}
    context['teams'] = getTeamsSecondRound(conf_name='UEFA')
    zone1 = getZoneData('A', 'UEFA', 'second')
    zone2 = getZoneData('B', 'UEFA', 'second')
    zone3 = getZoneData('C', 'UEFA', 'second')
    zone4 = getZoneData('D', 'UEFA', 'second')
    zone5 = getZoneData('E', 'UEFA', 'second')
    zone6 = getZoneData('F', 'UEFA', 'second')
    if len(zone1['teams']) == 4:
        context['zone1'] = zone1['teams']
    if len(zone2['teams']) == 4:
        context['zone2'] = zone2['teams']
    if len(zone3['teams']) == 4:
        context['zone3'] = zone3['teams']
    if len(zone4['teams']) == 4:
        context['zone4'] = zone4['teams']
    if len(zone5['teams']) == 4:
        context['zone5'] = zone5['teams']
    if len(zone6['teams']) == 4:
        context['zone6'] = zone6['teams']
    return render(request, 'europa/sndround.html', context)


def firstround(request):
    context = {}
    context['teams'] = getTeamsFirstRound(conf_name='UEFA')
    zone1 = getZoneData('A', 'UEFA', 'first')
    zone2 = getZoneData('B', 'UEFA', 'first')
    zoneWC = getZoneData('WC', 'UEFA', 'first')

    if len(zone1['teams']) == 5:
        context['zone1'] = zone1['teams']
    if len(zone2['teams']) == 5:
        context['zone2'] = zone2['teams']
    context['fixture'] = zoneWC['fixtures']

    return render(request, 'europa/fstround.html', context)


def teams(request):
    context = {}
    context['teams'] = getTeams(conf_name='UEFA')
    return render(request, 'europa/teamlist.html', context)


def updateProgress(request, id, stage):
    if request.method == 'POST':
        updateStage(id, stage)
    return redirect('europa.teams')


def firstRoundButton(request):
    if request.method == 'GET':
        context = {}
        context['teams'] = getTeamsFirstRound('UEFA')
        zone1, zone2 = firstRoundDraw(getTeamsFirstRound('UEFA'))
        random.shuffle(zone1)
        random.shuffle(zone2)
        createFixture(zone1, False, 'A', 'UEFA', 'first')
        createFixture(zone2, False, 'B', 'UEFA', 'first')
        context['zone1'] = zone1
        context['zone2'] = zone2

        return render(request, 'europa/fstround.html', context)


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

        return render(request, 'europa/sndround.html', context)


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

        return render(request, 'europa/thrround.html', context)


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

        return render(request, 'europa/finalround.html', context)


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
    teamId = request.GET.get('home')
    team = getTeamById(teamId)
    db.get_collection('Fixtures').update_one({'$and': [{'conf_name': 'UEFA'}, {'zone': 'WC'}, {'round': 'first'}]},
                                             {'$set': {
                                                 'fixtures.wildCard.match1.homeTeam.team': team[0]
                                             }})
    return firstround(request)


def setAwayWildCardTeam(request):
    db = db_conexion()
    teamId = request.GET.get('away')
    team = getTeamById(teamId)
    db.get_collection('Fixtures').update_one({'$and': [{'conf_name': 'UEFA'}, {'zone': 'WC'}, {'round': 'first'}]},
                                             {'$set': {
                                                 'fixtures.wildCard.match1.awayTeam.team': team[0]
                                             }})
    return firstround(request)
