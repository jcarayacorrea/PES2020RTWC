import random

from django.shortcuts import render, redirect
from utils import getTeams, updateStage, getTeamsFirstRound, getTeamsSecondRound, getTeamsThirdRound, getTeamsFinalRound


# Create your views here.
def finalround(request):
    context = {}
    context['teams'] = getTeamsFinalRound(conf_name='CAF')
    return render(request,'africa/finalround.html',context)

def thirdround(request):
    context = {}
    context['teams'] = getTeamsThirdRound(conf_name='CAF')
    return render(request,'africa/thrround.html',context)

def secondround(request):
    context = {}
    context['teams'] = getTeamsSecondRound(conf_name='CAF')
    return render(request,'africa/sndround.html',context)

def firstround(request):
    context = {}
    context['teams'] = getTeamsFirstRound(conf_name='CAF')
    return render(request,'africa/fstround.html',context)

def teams(request):
    context = {}
    context['teams'] = getTeams(conf_name='CAF')
    return render(request,'africa/teamlist.html',context)

def updateProgress(request,id, stage):
    if request.method == 'POST':
        updateStage(id,stage)
    return  redirect('africa.teams')

def firstRoundButton(request):
    if request.method == 'GET':
        context = {}
        context['teams'] = getTeamsFirstRound('UEFA')
        zone1, zone2 = firstRoundDraw(getTeamsFirstRound('UEFA'))
        random.shuffle(zone1)
        random.shuffle(zone2)

        context['zone1'] = zone1
        context['zone2'] = zone2


        return render(request,'europa/fstround.html',context)

def firstRoundDraw(teams):

    pool1 = [teams[0],teams[1]]
    pool2 = [teams[2], teams[3]]
    pool3 = [teams[4], teams[5]]
    pool4 = [teams[6], teams[7]]
    pool5 = [teams[8], teams[9]]

    random.shuffle(pool1)
    random.shuffle(pool2)
    random.shuffle(pool3)
    random.shuffle(pool4)
    random.shuffle(pool5)

    zone1 = [pool1[0],pool2[0],pool3[0],pool4[0],pool5[0]]
    zone2 = [pool1[1], pool2[1], pool3[1], pool4[1], pool5[1]]

    return zone1, zone2

def secondRoundButton(request):
    if request.method == 'GET':
        context = {}
        context['teams'] = getTeamsSecondRound('UEFA')
        zone1, zone2,zone3,zone4,zone5,zone6 = secondRoundDraw(getTeamsSecondRound('UEFA'))
        random.shuffle(zone1)
        random.shuffle(zone2)
        random.shuffle(zone3)
        random.shuffle(zone4)
        random.shuffle(zone5)
        random.shuffle(zone6)

        context['zone1'] = zone1
        context['zone2'] = zone2
        context['zone3'] = zone3
        context['zone4'] = zone4
        context['zone5'] = zone5
        context['zone6'] = zone6


        return render(request,'europa/sndround.html',context)

def secondRoundDraw(teams):

    pool1 = [teams[0],teams[1],teams[2],teams[3],teams[4],teams[5]]
    pool2 = [teams[6], teams[7],teams[8], teams[9],teams[10], teams[11]]
    pool3 = [teams[12], teams[13],teams[14], teams[15],teams[16], teams[17]]
    pool4 = [teams[18], teams[19],teams[20], teams[21],teams[22], teams[23]]


    random.shuffle(pool1)
    random.shuffle(pool2)
    random.shuffle(pool3)
    random.shuffle(pool4)


    zone1 = [pool1[0],pool2[0],pool3[0],pool4[0]]
    zone2 = [pool1[1], pool2[1], pool3[1], pool4[1]]
    zone3 = [pool1[2], pool2[2], pool3[2], pool4[2]]
    zone4 = [pool1[3], pool2[3], pool3[3], pool4[3]]
    zone5 = [pool1[4], pool2[4], pool3[4], pool4[4]]
    zone6 = [pool1[5], pool2[5], pool3[5], pool4[5]]

    return zone1, zone2,zone3,zone4,zone5,zone6

def thirdRoundButton(request):
    if request.method == 'GET':
        context = {}
        context['teams'] = getTeamsThirdRound('UEFA')
        zone1, zone2,zone3,zone4,zone5,zone6,zone7, zone8 = thirdRoundDraw(getTeamsThirdRound('UEFA'))
        random.shuffle(zone1)
        random.shuffle(zone2)
        random.shuffle(zone3)
        random.shuffle(zone4)
        random.shuffle(zone5)
        random.shuffle(zone6)
        random.shuffle(zone7)
        random.shuffle(zone8)

        context['zone1'] = zone1
        context['zone2'] = zone2
        context['zone3'] = zone3
        context['zone4'] = zone4
        context['zone5'] = zone5
        context['zone6'] = zone6
        context['zone7'] = zone7
        context['zone8'] = zone8


        return render(request,'europa/thrround.html',context)

def thirdRoundDraw(teams):

    pool1 = [teams[0],teams[1],teams[2],teams[3],teams[4],teams[5],teams[6], teams[7]]
    pool2 = [teams[8], teams[9],teams[10], teams[11],teams[12], teams[13],teams[14], teams[15]]
    pool3 = [teams[16], teams[17],teams[18], teams[19],teams[20], teams[21],teams[22],teams[23]]


    random.shuffle(pool1)
    random.shuffle(pool2)
    random.shuffle(pool3)



    zone1 = [pool1[0],pool2[0],pool3[0]]
    zone2 = [pool1[1], pool2[1], pool3[1]]
    zone3 = [pool1[2], pool2[2], pool3[2]]
    zone4 = [pool1[3], pool2[3], pool3[3]]
    zone5 = [pool1[4], pool2[4], pool3[4]]
    zone6 = [pool1[5], pool2[5], pool3[5]]
    zone7 = [pool1[6], pool2[6], pool3[6]]
    zone8 = [pool1[7], pool2[7], pool3[7]]

    return zone1, zone2,zone3,zone4,zone5,zone6,zone7,zone8

def finalRoundButton(request):
    if request.method == 'GET':
        context = {}
        context['teams'] = getTeamsFinalRound('UEFA')
        zone1, zone2,zone3,zone4 = finalRoundDraw(getTeamsFinalRound('UEFA'))
        random.shuffle(zone1)
        random.shuffle(zone2)
        random.shuffle(zone3)
        random.shuffle(zone4)


        context['zone1'] = zone1
        context['zone2'] = zone2
        context['zone3'] = zone3
        context['zone4'] = zone4



        return render(request,'europa/finalround.html',context)

def finalRoundDraw(teams):

    pool1 = [teams[0],teams[1],teams[2],teams[3]]
    pool2 = [teams[4],teams[5],teams[6], teams[7]]
    pool3 = [teams[8], teams[9],teams[10], teams[11]]
    pool4 = [teams[12], teams[13],teams[14], teams[15]]
    pool5 = [teams[16], teams[17], teams[18], teams[19]]


    random.shuffle(pool1)
    random.shuffle(pool2)
    random.shuffle(pool3)
    random.shuffle(pool4)
    random.shuffle(pool5)



    zone1 = [pool1[0],pool2[0],pool3[0],pool4[0],pool5[0]]
    zone2 = [pool1[1], pool2[1], pool3[1],pool4[1],pool5[1]]
    zone3 = [pool1[2], pool2[2], pool3[2],pool4[2],pool5[2]]
    zone4 = [pool1[3], pool2[3], pool3[3],pool4[3],pool5[3]]


    return zone1, zone2,zone3,zone4

