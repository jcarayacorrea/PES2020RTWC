import random

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from operator import itemgetter
from utils import getTeams, updateStage, getTeamsCopaAmerica


# Create your views here.
def teams(request):
    context = {}
    context['teams'] = getTeams(conf_name='CONMEBOL')
    return render(request, 'sudamerica/teamlist.html', context)


def copaAmerica(request):
    context = {}
    context['teams'] = getTeamsCopaAmerica()
    return render(request, 'sudamerica/copaamerica.html', context)


def updateProgress(request, id, stage):
    if request.method == 'POST':
        updateStage(id, stage)
    return redirect('sudamerica.finalround')


def copaAmericaButton(request):
    if request.method == 'GET':
        context = {}
        context['teams'] = getTeamsCopaAmerica()
        zone1, zone2, zone3, zone4 = copaAmericaDraw(getTeamsCopaAmerica())
        random.shuffle(zone1)
        random.shuffle(zone2)
        random.shuffle(zone3)
        random.shuffle(zone4)

        context['zone1'] = zone1
        context['zone2'] = zone2
        context['zone3'] = zone3
        context['zone4'] = zone4

        return render(request, 'sudamerica/copaamerica.html', context)


def copaAmericaDraw(teams):
    sudamerica = [team for team in teams if team['conf_name'] == 'CONMEBOL']
    ncamerica = [team for team in teams if team['conf_name'] == 'CONCACAF']
    sudSeed = sudamerica[0:2]
    ncSeed = ncamerica[0:2]
    restTeams = sorted(sudamerica[2:10] + ncamerica[2:6], key=itemgetter('fifa_nation_rank'), reverse=False)

    pool2 = restTeams[0:4]
    pool3 = restTeams[4:8]
    pool4 = restTeams[8:12]

    random.shuffle(sudSeed)
    random.shuffle(ncSeed)
    random.shuffle(pool2)
    random.shuffle(pool3)
    random.shuffle(pool4)

    zone1 = [sudSeed[0], pool2[0], pool3[0], pool4[0]]
    zone2 = [ncSeed[0], pool2[1], pool3[1], pool4[1]]
    zone3 = [ncSeed[1], pool2[2], pool3[2], pool4[2]]
    zone4 = [sudSeed[1], pool2[3], pool3[3], pool4[3]]

    return zone1, zone2, zone3, zone4
