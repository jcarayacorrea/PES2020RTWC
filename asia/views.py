import random

from django.shortcuts import render, redirect
from utils import db_conexion, getTeams, updateStage, getTeamsFirstRound, getTeamsSecondRound, getTeamsThirdRound, \
    getTeamsFinalRound


# Create your views here.
def finalround(request):
    context = {}
    context['teams'] = getTeamsFinalRound(conf_name='AFC')
    return render(request, 'asia/finalround.html', context)


def thirdround(request):
    context = {}
    context['teams'] = getTeamsThirdRound(conf_name='AFC')
    return render(request, 'asia/thrround.html', context)


def secondround(request):
    context = {}
    context['teams'] = getTeamsSecondRound(conf_name='AFC')
    return render(request, 'asia/sndround.html', context)


def firstround(request):
    context = {}
    context['teams'] = getTeamsFirstRound(conf_name='AFC')
    return render(request, 'asia/fstround.html', context)


def teams(request):
    context = {}
    context['teams'] = getTeams(conf_name='AFC')
    return render(request, 'asia/teamlist.html', context)


def updateProgress(request, id, stage):
    if request.method == 'POST':
        updateStage(id, stage)
    return redirect('asia.teams')


def firstRoundDraw(teams):
    pool1 = [teams[0], teams[1], teams[2]]
    pool2 = [teams[3], teams[4], teams[5]]
    pool3 = [teams[6], teams[7], teams[8]]
    pool4 = [teams[9], teams[10], teams[11]]

    random.shuffle(pool1)
    random.shuffle(pool2)
    random.shuffle(pool3)
    random.shuffle(pool4)

    zoneA = [pool1[0], pool2[0], pool3[0], pool4[0]]
    zoneB = [pool1[1], pool2[1], pool3[1], pool4[1]]
    zoneC = [pool1[2], pool2[2], pool3[2], pool4[2]]

    return random.shuffle(zoneA), random.shuffle(zoneB), random.shuffle(zoneC)

