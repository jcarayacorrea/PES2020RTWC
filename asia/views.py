import random

from django.shortcuts import render, redirect
from utils import db_conexion, getTeams, updateStage, getTeamsFirstRound, getTeamsSecondRound, getTeamsThirdRound, \
    getTeamsFinalRound
from fixtures import createFixture, getZoneData


# Create your views here.
def finalround(request):
    context = {}
    context['teams'] = getTeamsFinalRound(conf_name='AFC')
    zone1 = getZoneData('A', 'AFC', 'third')
    zone2 = getZoneData('B', 'AFC', 'third')
    zone3 = getZoneData('C', 'AFC', 'third')
    zone4 = getZoneData('D', 'AFC', 'third')
    if len(zone1['teams']) == 4:
        context['zone1'] = zone1['teams']
    if len(zone2['teams']) == 4:
        context['zone2'] = zone2['teams']
    if len(zone3['teams']) == 4:
        context['zone3'] = zone3['teams']
    if len(zone4['teams']) == 4:
        context['zone4'] = zone4['teams']
    return render(request, 'asia/finalround.html', context)


def thirdround(request):
    context = {}
    context['teams'] = getTeamsThirdRound(conf_name='AFC')
    zone1 = getZoneData('A', 'AFC', 'third')
    zone2 = getZoneData('B', 'AFC', 'third')
    zone3 = getZoneData('C', 'AFC', 'third')
    zone4 = getZoneData('D', 'AFC', 'third')
    zone5 = getZoneData('E', 'AFC', 'third')
    zone6 = getZoneData('F', 'AFC', 'third')
    zone7 = getZoneData('G', 'AFC', 'third')
    zone8 = getZoneData('H', 'AFC', 'third')

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
    if len(zone7['teams']) == 4:
        context['zone7'] = zone7['teams']
    if len(zone8['teams']) == 4:
        context['zone8'] = zone8['teams']
    return render(request, 'asia/thrround.html', context)


def secondround(request):
    context = {}
    context['teams'] = getTeamsSecondRound(conf_name='AFC')
    zone1 = getZoneData('A', 'AFC', 'second')
    zone2 = getZoneData('B', 'AFC', 'second')
    zone3 = getZoneData('C', 'AFC', 'second')
    zone4 = getZoneData('D', 'AFC', 'second')
    zone5 = getZoneData('E', 'AFC', 'second')
    zone6 = getZoneData('F', 'AFC', 'second')
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
    return render(request, 'asia/sndround.html', context)


def firstround(request):
    context = {
        'conf': 'AFC',
        'round': 'first',
        'zone': 'A'
    }
    context['teams'] = getTeamsFirstRound(conf_name='AFC')
    zone1 = getZoneData('A', 'AFC', 'first')
    if len(zone1['teams']) == 4:
        context['zone1'] = zone1['teams']

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
        context['teams'] = getTeamsFirstRound('AFC')
        zone1 = firstRoundDraw(getTeamsFirstRound('AFC'))
        random.shuffle(zone1)
        createFixture(zone1, False, 'A', 'AFC', 'first')
        context['zone1'] = zone1
        return render(request, 'asia/fstround.html', context)


def firstRoundDraw(teams):
    zone1 = teams

    return zone1


def secondRoundButton(request):
    if request.method == 'GET':
        context = {}
        context['teams'] = getTeamsSecondRound('AFC')
        zone1, zone2, zone3, zone4, zone5, zone6 = secondRoundDraw(getTeamsSecondRound('AFC'))
        random.shuffle(zone1)
        random.shuffle(zone2)
        random.shuffle(zone3)
        random.shuffle(zone4)
        random.shuffle(zone5)
        random.shuffle(zone6)
        createFixture(zone1, True, 'A', 'AFC', 'second')
        createFixture(zone2, True, 'B', 'AFC', 'second')
        createFixture(zone3, True, 'C', 'AFC', 'second')
        createFixture(zone4, True, 'D', 'AFC', 'second')
        createFixture(zone5, True, 'E', 'AFC', 'second')
        createFixture(zone6, True, 'F', 'AFC', 'second')

        context['zone1'] = zone1
        context['zone2'] = zone2
        context['zone3'] = zone3
        context['zone4'] = zone4
        context['zone5'] = zone5
        context['zone6'] = zone6

        return render(request, 'asia/sndround.html', context)


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
        context['teams'] = getTeamsThirdRound('AFC')
        zone1, zone2, zone3, zone4, zone5, zone6, zone7, zone8 = thirdRoundDraw(getTeamsThirdRound('AFC'))
        random.shuffle(zone1)
        random.shuffle(zone2)
        random.shuffle(zone3)
        random.shuffle(zone4)
        random.shuffle(zone5)
        random.shuffle(zone6)
        random.shuffle(zone7)
        random.shuffle(zone8)
        createFixture(zone1, True, 'A', 'AFC', 'third')
        createFixture(zone2, True, 'B', 'AFC', 'third')
        createFixture(zone3, True, 'C', 'AFC', 'third')
        createFixture(zone4, True, 'D', 'AFC', 'third')
        createFixture(zone5, True, 'E', 'AFC', 'third')
        createFixture(zone6, True, 'F', 'AFC', 'third')
        createFixture(zone7, True, 'G', 'AFC', 'third')
        createFixture(zone8, True, 'H', 'AFC', 'third')

        context['zone1'] = zone1
        context['zone2'] = zone2
        context['zone3'] = zone3
        context['zone4'] = zone4
        context['zone5'] = zone5
        context['zone6'] = zone6
        context['zone7'] = zone7
        context['zone8'] = zone8

        return render(request, 'asia/thrround.html', context)


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
        context['teams'] = getTeamsFinalRound('AFC')
        zone1, zone2, zone3, zone4 = finalRoundDraw(getTeamsFinalRound('AFC'))
        random.shuffle(zone1)
        random.shuffle(zone2)
        random.shuffle(zone3)
        random.shuffle(zone4)
        createFixture(zone1, True, 'A', 'AFC', 'final')
        createFixture(zone2, True, 'B', 'AFC', 'final')
        createFixture(zone3, True, 'C', 'AFC', 'final')
        createFixture(zone4, True, 'D', 'AFC', 'final')

        context['zone1'] = zone1
        context['zone2'] = zone2
        context['zone3'] = zone3
        context['zone4'] = zone4

        return render(request, 'asia/finalround.html', context)


def finalRoundDraw(teams):
    pool1 = [teams[0], teams[1], teams[2], teams[3]]
    pool2 = [teams[4], teams[5], teams[6], teams[7]]
    pool3 = [teams[8], teams[9], teams[10], teams[11]]
    pool4 = [teams[12], teams[13], teams[14], teams[15]]

    random.shuffle(pool1)
    random.shuffle(pool2)
    random.shuffle(pool3)
    random.shuffle(pool4)

    zone1 = [pool1[0], pool2[0], pool3[0], pool4[0]]
    zone2 = [pool1[1], pool2[1], pool3[1], pool4[1]]
    zone3 = [pool1[2], pool2[2], pool3[2], pool4[2]]
    zone4 = [pool1[3], pool2[3], pool3[3], pool4[3]]

    return zone1, zone2, zone3, zone4
