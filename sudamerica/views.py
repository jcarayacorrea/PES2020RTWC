import random

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from utils import getTeams, updateStage,getTeamsCopaAmerica


# Create your views here.
def finalround(request):
    context = {}
    context['teams'] = getTeams(conf_name='CONMEBOL')
    return render(request, 'sudamerica/finalround.html', context)

def copaAmerica(request):
    context = {}
    context['teams'] = getTeamsCopaAmerica()
    return render(request, 'sudamerica/copaamerica.html', context)


def updateProgress(request,id, stage):
    if request.method == 'POST':
        updateStage(id,stage)
    return   redirect('sudamerica.finalround')

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
