import random

from django.shortcuts import render, redirect

from fixtures import getZoneData, createFixture
from utils import updateStage, getTeams, getTeamsFirstRound, getTeamsFinalRound


# Create your views here.
def finalround(request):
    context = {}
    context['teams'] = getTeamsFinalRound(conf_name='OFC')
    zone1 = getZoneData('A', 'OFC', 'final')
    zone2 = getZoneData('B', 'OFC', 'final')
    if len(zone1['teams']) == 4:
        context['zone1'] = zone1['teams']
    if len(zone2['teams']) == 4:
        context['zone2'] = zone2['teams']
    return render(request, 'oceania/finalround.html', context)


def firstround(request):
    context = {}
    context['teams'] = getTeamsFirstRound(conf_name='OFC')
    zone1 = getZoneData('A', 'OFC', 'first')
    if len(zone1['teams']) == 5:
        context['zone1'] = zone1['teams']
    return render(request, 'oceania/fstround.html', context)


def teams(request):
    context = {}
    context['teams'] = getTeams(conf_name='OFC')
    return render(request, 'oceania/teamlist.html', context)


def updateProgress(request, id, stage):
    if request.method == 'POST':
        updateStage(id, stage)
    return redirect('oceania.teams')


def firstRoundButton(request):
    if request.method == 'GET':
        context = {}
        context['teams'] = getTeamsFirstRound('OFC')
        zone1 = firstRoundDraw(getTeamsFirstRound('OFC'))
        random.shuffle(zone1)
        createFixture(zone1, False, 'A', 'OFC', 'first')
        context['zone1'] = zone1

        return render(request, 'oceania/fstround.html', context)


def firstRoundDraw(teams):
    zone1 = teams

    return zone1


def finalRoundButton(request):
    if request.method == 'GET':
        context = {}
        context['teams'] = getTeamsFinalRound('OFC')
        zone1, zone2 = finalRoundDraw(getTeamsFinalRound('OFC'))
        random.shuffle(zone1)
        random.shuffle(zone2)
        createFixture(zone1, True, 'A', 'OFC', 'final')
        createFixture(zone1, True, 'B', 'OFC', 'final')
        context['zone1'] = zone1
        context['zone2'] = zone2

        return render(request, 'oceania/finalround.html', context)


def finalRoundDraw(teams):
    pool1 = [teams[0], teams[1]]
    pool2 = [teams[2], teams[3]]
    pool3 = [teams[4], teams[5]]
    pool4 = [teams[6], teams[7]]

    random.shuffle(pool1)
    random.shuffle(pool2)
    random.shuffle(pool3)
    random.shuffle(pool4)

    zone1 = [pool1[0], pool2[0], pool3[0], pool4[0]]
    zone2 = [pool1[1], pool2[1], pool3[1], pool4[1]]

    return zone1, zone2
