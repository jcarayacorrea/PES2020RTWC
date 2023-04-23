import random

from django.shortcuts import render, redirect

from fixtures import getZoneData, createFixture
from utils import getTeams, updateStage, getTeamsFirstRound, getTeamsSecondRound, getTeamsThirdRound, getTeamsFinalRound


# Create your views here.
def finalround(request):
    context = {}
    context['teams'] = getTeamsFinalRound(conf_name='CAF')
    zone1 = getZoneData('A', 'CAF', 'final')
    zone2 = getZoneData('B', 'CAF', 'final')
    zone3 = getZoneData('C', 'CAF', 'final')
    zone4 = getZoneData('D', 'CAF', 'final')
    zone5 = getZoneData('E', 'CAF', 'final')
    if len(zone1['teams']) == 5:
        context['zone1'] = zone1['teams']
    if len(zone2['teams']) == 5:
        context['zone2'] = zone2['teams']
    if len(zone3['teams']) == 5:
        context['zone3'] = zone3['teams']
    if len(zone4['teams']) == 5:
        context['zone4'] = zone4['teams']
    if len(zone5['teams']) == 5:
        context['zone5'] = zone5['teams']
    return render(request, 'africa/finalround.html', context)


def thirdround(request):
    context = {}
    context['teams'] = getTeamsThirdRound(conf_name='CAF')
    zone1 = getZoneData('A', 'CAF', 'third')
    zone2 = getZoneData('B', 'CAF', 'third')
    zone3 = getZoneData('C', 'CAF', 'third')
    zone4 = getZoneData('D', 'CAF', 'third')
    zone5 = getZoneData('E', 'CAF', 'third')
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
    return render(request, 'africa/thrround.html', context)


def secondround(request):
    context = {}
    context['teams'] = getTeamsSecondRound(conf_name='CAF')
    zone1 = getZoneData('A', 'CAF', 'second')
    zone2 = getZoneData('B', 'CAF', 'second')
    zone3 = getZoneData('C', 'CAF', 'second')
    zone4 = getZoneData('D', 'CAF', 'second')
    zone5 = getZoneData('E', 'CAF', 'second')
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
    return render(request, 'africa/sndround.html', context)


def firstround(request):
    context = {}
    context['teams'] = getTeamsFirstRound(conf_name='CAF')
    zone1 = getZoneData('A', 'CAF', 'first')
    zone2 = getZoneData('B', 'CAF', 'first')
    zone3 = getZoneData('C', 'CAF', 'first')

    if len(zone1['teams']) == 4:
        context['zone1'] = zone1['teams']
    if len(zone2['teams']) == 4:
        context['zone2'] = zone2['teams']
    if len(zone3['teams']) == 4:
        context['zone3'] = zone3['teams']

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
        context['teams'] = getTeamsFirstRound('CAF')
        zone1, zone2, zone3 = firstRoundDraw(getTeamsFirstRound('CAF'))
        random.shuffle(zone1)
        random.shuffle(zone2)
        random.shuffle(zone3)

        createFixture(zone1, False, 'A', 'CAF', 'first')
        createFixture(zone2, False, 'B', 'CAF', 'first')
        createFixture(zone3, False, 'C', 'CAF', 'first')

        context['zone1'] = zone1
        context['zone2'] = zone2
        context['zone3'] = zone3

        return render(request, 'africa/fstround.html', context)


def firstRoundDraw(teams):
    pool1 = [teams[0], teams[1], teams[2]]
    pool2 = [teams[3], teams[4], teams[5]]
    pool3 = [teams[6], teams[7], teams[8]]
    pool4 = [teams[9], teams[10], teams[11]]

    random.shuffle(pool1)
    random.shuffle(pool2)
    random.shuffle(pool3)
    random.shuffle(pool4)

    zone1 = [pool1[0], pool2[0], pool3[0], pool4[0]]
    zone2 = [pool1[1], pool2[1], pool3[1], pool4[1]]
    zone3 = [pool1[2], pool2[2], pool3[2], pool4[2]]

    return zone1, zone2, zone3


def secondRoundButton(request):
    if request.method == 'GET':
        context = {}
        context['teams'] = getTeamsSecondRound('CAF')
        zone1, zone2, zone3, zone4, zone5 = secondRoundDraw(getTeamsSecondRound('CAF'))
        random.shuffle(zone1)
        random.shuffle(zone2)
        random.shuffle(zone3)
        random.shuffle(zone4)
        random.shuffle(zone5)

        createFixture(zone1, True, 'A', 'CAF', 'second')
        createFixture(zone2, True, 'B', 'CAF', 'second')
        createFixture(zone3, True, 'C', 'CAF', 'second')
        createFixture(zone4, True, 'D', 'CAF', 'second')
        createFixture(zone5, True, 'E', 'CAF', 'second')

        context['zone1'] = zone1
        context['zone2'] = zone2
        context['zone3'] = zone3
        context['zone4'] = zone4
        context['zone5'] = zone5

        return render(request, 'africa/sndround.html', context)


def secondRoundDraw(teams):
    pool1 = [teams[0], teams[1], teams[2], teams[3], teams[4]]
    pool2 = [teams[5], teams[6], teams[7], teams[8], teams[9]]
    pool3 = [teams[10], teams[11], teams[12], teams[13], teams[14]]
    pool4 = [teams[15], teams[16], teams[17], teams[18], teams[19]]

    random.shuffle(pool1)
    random.shuffle(pool2)
    random.shuffle(pool3)
    random.shuffle(pool4)

    zone1 = [pool1[0], pool2[0], pool3[0], pool4[0]]
    zone2 = [pool1[1], pool2[1], pool3[1], pool4[1]]
    zone3 = [pool1[2], pool2[2], pool3[2], pool4[2]]
    zone4 = [pool1[3], pool2[3], pool3[3], pool4[3]]
    zone5 = [pool1[4], pool2[4], pool3[4], pool4[4]]
    return zone1, zone2, zone3, zone4, zone5


def thirdRoundButton(request):
    if request.method == 'GET':
        context = {}
        context['teams'] = getTeamsThirdRound('CAF')
        zone1, zone2, zone3, zone4, zone5 = thirdRoundDraw(getTeamsThirdRound('CAF'))
        random.shuffle(zone1)
        random.shuffle(zone2)
        random.shuffle(zone3)
        random.shuffle(zone4)
        random.shuffle(zone5)

        createFixture(zone1, True, 'A', 'CAF', 'third')
        createFixture(zone2, True, 'B', 'CAF', 'third')
        createFixture(zone3, True, 'C', 'CAF', 'third')
        createFixture(zone4, True, 'D', 'CAF', 'third')
        createFixture(zone5, True, 'E', 'CAF', 'third')

        context['zone1'] = zone1
        context['zone2'] = zone2
        context['zone3'] = zone3
        context['zone4'] = zone4
        context['zone5'] = zone5

        return render(request, 'africa/thrround.html', context)


def thirdRoundDraw(teams):
    pool1 = [teams[0], teams[1], teams[2], teams[3], teams[4]]
    pool2 = [teams[5], teams[6], teams[7], teams[8], teams[9]]
    pool3 = [teams[10], teams[11], teams[12], teams[13], teams[14]]
    pool4 = [teams[15], teams[16], teams[17], teams[18], teams[19]]

    random.shuffle(pool1)
    random.shuffle(pool2)
    random.shuffle(pool3)
    random.shuffle(pool4)

    zone1 = [pool1[0], pool2[0], pool3[0], pool4[0]]
    zone2 = [pool1[1], pool2[1], pool3[1], pool4[1]]
    zone3 = [pool1[2], pool2[2], pool3[2], pool4[2]]
    zone4 = [pool1[3], pool2[3], pool3[3], pool4[3]]
    zone5 = [pool1[4], pool2[4], pool3[4], pool4[4]]
    return zone1, zone2, zone3, zone4, zone5


def finalRoundButton(request):
    if request.method == 'GET':
        context = {}
        context['teams'] = getTeamsFinalRound('CAF')
        zone1, zone2, zone3, zone4, zone5 = finalRoundDraw(getTeamsFinalRound('CAF'))
        random.shuffle(zone1)
        random.shuffle(zone2)
        random.shuffle(zone3)
        random.shuffle(zone4)
        random.shuffle(zone5)

        createFixture(zone1, True, 'A', 'CAF', 'final')
        createFixture(zone2, True, 'B', 'CAF', 'final')
        createFixture(zone3, True, 'C', 'CAF', 'final')
        createFixture(zone4, True, 'D', 'CAF', 'final')
        createFixture(zone5, True, 'E', 'CAF', 'final')

        context['zone1'] = zone1
        context['zone2'] = zone2
        context['zone3'] = zone3
        context['zone4'] = zone4
        context['zone5'] = zone5

        return render(request, 'africa/finalround.html', context)


def finalRoundDraw(teams):
    pool1 = [teams[0], teams[1], teams[2], teams[3], teams[4]]
    pool2 = [teams[5], teams[6], teams[7], teams[8], teams[9]]
    pool3 = [teams[10], teams[11], teams[12], teams[13], teams[14]]
    pool4 = [teams[15], teams[16], teams[17], teams[18], teams[19]]
    pool5 = [teams[20], teams[21], teams[22], teams[23], teams[24]]

    random.shuffle(pool1)
    random.shuffle(pool2)
    random.shuffle(pool3)
    random.shuffle(pool4)
    random.shuffle(pool5)

    zone1 = [pool1[0], pool2[0], pool3[0], pool4[0], pool5[0]]
    zone2 = [pool1[1], pool2[1], pool3[1], pool4[1], pool5[1]]
    zone3 = [pool1[2], pool2[2], pool3[2], pool4[2], pool5[2]]
    zone4 = [pool1[3], pool2[3], pool3[3], pool4[3], pool5[3]]
    zone5 = [pool1[4], pool2[4], pool3[4], pool4[4], pool5[4]]

    return zone1, zone2, zone3, zone4, zone5
