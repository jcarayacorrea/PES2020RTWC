import random

from django.shortcuts import render, redirect

from fixtures import getZoneData, create_fixture
from utils import updateStage, getTeams, getTeamsFinalRound, getTeamsFirstRound


# Create your views here.
def finalround(request):
    context = {}
    context['teams'] = getTeamsFinalRound(conf_name='CONCACAF')
    zone1 = getZoneData('A', 'CONCACAF', 'final')
    zone2 = getZoneData('B', 'CONCACAF', 'final')
    zone3 = getZoneData('C', 'CONCACAF', 'final')
    if len(zone1['teams']) == 5:
        context['zone1'] = zone1['teams']
    if len(zone2['teams']) == 5:
        context['zone2'] = zone2['teams']
    if len(zone3['teams']) == 5:
        context['zone3'] = zone3['teams']
    return render(request, 'ncamerica/finalround.html', context)


def firstround(request):
    context = {}
    context['teams'] = getTeamsFirstRound(conf_name='CONCACAF')
    zone1 = getZoneData('A', 'CONCACAF', 'first')
    zone2 = getZoneData('B', 'CONCACAF', 'first')
    zone3 = getZoneData('C', 'CONCACAF', 'first')
    zone4 = getZoneData('D', 'CONCACAF', 'first')
    zone5 = getZoneData('E', 'CONCACAF', 'first')
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
    return render(request, 'ncamerica/fstround.html', context)


def teams(request):
    context = {}
    context['teams'] = getTeams(conf_name='CONCACAF')
    return render(request, 'ncamerica/teamlist.html', context)


def updateProgress(request, id, stage):
    if request.method == 'POST':
        updateStage(id, stage)
    return redirect('ncamerica.teams')


def firstRoundButton(request):
    if request.method == 'GET':
        context = {}
        context['teams'] = getTeamsFirstRound('CONCACAF')
        zone1, zone2, zone3, zone4, zone5 = firstRoundDraw(getTeamsFirstRound('CONCACAF'))
        random.shuffle(zone1)
        random.shuffle(zone2)
        random.shuffle(zone3)
        random.shuffle(zone4)
        random.shuffle(zone5)

        createFixture(zone1, True, 'A', 'CONCACAF', 'first')
        createFixture(zone2, True, 'B', 'CONCACAF', 'first')
        createFixture(zone3, True, 'C', 'CONCACAF', 'first')
        createFixture(zone4, True, 'D', 'CONCACAF', 'first')
        createFixture(zone5, True, 'E', 'CONCACAF', 'first')

        context['zone1'] = zone1
        context['zone2'] = zone2
        context['zone3'] = zone3
        context['zone4'] = zone4
        context['zone5'] = zone5

    return firstround(request)


def firstRoundDraw(teams):
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


def finalRoundButton(request):
    if request.method == 'GET':
        context = {}
        context['teams'] = getTeamsFinalRound('CONCACAF')
        zone1, zone2, zone3 = finalRoundDraw(getTeamsFinalRound('CONCACAF'))
        random.shuffle(zone1)
        random.shuffle(zone2)
        random.shuffle(zone3)

        createFixture(zone1, True, 'A', 'CONCACAF', 'final')
        createFixture(zone2, True, 'B', 'CONCACAF', 'final')
        createFixture(zone3, True, 'C', 'CONCACAF', 'final')
        context['zone1'] = zone1
        context['zone2'] = zone2
        context['zone3'] = zone3

        return finalround(request)


def finalRoundDraw(teams):
    pool1 = [teams[0], teams[1], teams[2]]
    pool2 = [teams[3], teams[4], teams[5]]
    pool3 = [teams[6], teams[7], teams[8]]
    pool4 = [teams[9], teams[10], teams[11]]
    pool5 = [teams[12], teams[13], teams[14]]

    random.shuffle(pool1)
    random.shuffle(pool2)
    random.shuffle(pool3)
    random.shuffle(pool4)
    random.shuffle(pool5)

    zone1 = [pool1[0], pool2[0], pool3[0], pool4[0], pool5[0]]
    zone2 = [pool1[1], pool2[1], pool3[1], pool4[1], pool5[1]]
    zone3 = [pool1[2], pool2[2], pool3[2], pool4[2], pool5[2]]

    return zone1, zone2, zone3
