import random

from django.http import HttpResponse
from django.shortcuts import render, redirect

from fixtures import createPlayOffMatches, getZoneData
from utils import getTeamsMainDraw, getTeamsPlayoff


# Create your views here.
def maindraw(request):
    context = {}
    context['teams'] = getTeamsMainDraw()
    return render(request, 'worldcup/maindraw.html', context)


def playoff(request):
    context = {}
    context['teams'] = getTeamsPlayoff()
    playoffData = getZoneData('P', 'FIFA', 'playoff')
    context['fixture'] = playoffData['fixtures']
    return render(request, 'worldcup/playoff.html', context)


def maindrawButton(request):

    if request.method == 'GET':
        context = {}
        context['teams'] = getTeamsMainDraw()
        try:
            zoneA, zoneB, zoneC, zoneD, zoneE, zoneF, zoneG, zoneH = draw(getTeamsMainDraw())
        except:
            print("Error favor intentar nuevamente....")
            return maindraw(request)

        random.shuffle(zoneA)
        random.shuffle(zoneB)
        random.shuffle(zoneC)
        random.shuffle(zoneD)
        random.shuffle(zoneE)
        random.shuffle(zoneF)
        random.shuffle(zoneG)
        random.shuffle(zoneH)
        context['zoneA'] = zoneA
        context['zoneB'] = zoneB
        context['zoneC'] = zoneC
        context['zoneD'] = zoneD
        context['zoneE'] = zoneE
        context['zoneF'] = zoneF
        context['zoneG'] = zoneG
        context['zoneH'] = zoneH

        return render(request, 'worldcup/maindraw.html', context)


def playoffButton(request):
    if request.method == 'GET':
        context = {}
        context['teams'] = getTeamsPlayoff()
        zone1, zone2, zone3, zone4, zone5 = playoffDraw(getTeamsPlayoff())
        random.shuffle(zone1)
        random.shuffle(zone2)
        random.shuffle(zone3)
        random.shuffle(zone4)
        random.shuffle(zone5)
        createPlayOffMatches(getTeamsPlayoff(), zone1, zone2, zone3, zone4, zone5)
        playoffData = getZoneData('P', 'FIFA', 'playoff')
        context['fixture'] = playoffData['fixtures']

        return render(request, 'worldcup/playoff.html', context)


def draw(teams):
    pool1 = [teams[0], teams[1], teams[2], teams[3], teams[4], teams[5], teams[6], teams[7]]
    pool2 = [teams[8], teams[9], teams[10], teams[11], teams[12], teams[13], teams[14], teams[15]]
    pool3 = [teams[16], teams[17], teams[18], teams[19], teams[20], teams[21], teams[22], teams[23]]
    pool4 = [teams[24], teams[25], teams[26], teams[27], teams[28], teams[29], teams[30], teams[31]]
    random.shuffle(pool1)
    zoneA = [pool1[0]]
    zoneB = [pool1[1]]
    zoneC = [pool1[2]]
    zoneD = [pool1[3]]
    zoneE = [pool1[4]]
    zoneF = [pool1[5]]
    zoneG = [pool1[6]]
    zoneH = [pool1[7]]
    random.shuffle(pool2)
    for team in pool2:
        result = setTeamPosition(team['conf_name'], zoneA, zoneB, zoneC, zoneD, zoneE, zoneF, zoneG, zoneH,
                                 maxlength=2, teamsCount=countTeams(team['conf_name'], getTeamsMainDraw()))
        match (result):
            case 'A':
                zoneA.append(team)
            case 'B':
                zoneB.append(team)
            case 'C':
                zoneC.append(team)
            case 'D':
                zoneD.append(team)
            case 'E':
                zoneE.append(team)
            case 'F':
                zoneF.append(team)
            case 'G':
                zoneG.append(team)
            case 'H':
                zoneH.append(team)
    random.shuffle(pool3)
    for team in pool3:
        result = setTeamPosition(team['conf_name'], zoneA, zoneB, zoneC, zoneD, zoneE, zoneF, zoneG, zoneH,
                                 maxlength=3, teamsCount=countTeams(team['conf_name'], getTeamsMainDraw()))
        match (result):
            case 'A':
                zoneA.append(team)
            case 'B':
                zoneB.append(team)
            case 'C':
                zoneC.append(team)
            case 'D':
                zoneD.append(team)
            case 'E':
                zoneE.append(team)
            case 'F':
                zoneF.append(team)
            case 'G':
                zoneG.append(team)
            case 'H':
                zoneH.append(team)
    random.shuffle(pool4)
    for team in pool4:
        result = setTeamPosition(team['conf_name'], zoneA, zoneB, zoneC, zoneD, zoneE, zoneF, zoneG, zoneH,
                                 maxlength=4, teamsCount=countTeams(team['conf_name'], getTeamsMainDraw()))
        match (result):
            case 'A':
                zoneA.append(team)
            case 'B':
                zoneB.append(team)
            case 'C':
                zoneC.append(team)
            case 'D':
                zoneD.append(team)
            case 'E':
                zoneE.append(team)
            case 'F':
                zoneF.append(team)
            case 'G':
                zoneG.append(team)
            case 'H':
                zoneH.append(team)

    if (len(zoneA) != 4) or (len(zoneB) != 4) or (len(zoneC) != 4) or (len(zoneD) != 4) or (len(zoneE) != 4) \
            or (len(zoneF) != 4) or (len(zoneG) != 4) or (len(zoneH) != 4):
        draw(teams)
    else:
        return zoneA, zoneB, zoneC, zoneD, zoneE, zoneF, zoneG, zoneH


def setTeamPosition(conf_name, a, b, c, d, e, f, g, h, maxlength, teamsCount):
    zones = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    try:
        if (filterConfList(conf_name, a, teamsCount) == True or len(a) == maxlength) and len(zones) > 1:
            zones.remove('A')
        if (filterConfList(conf_name, b, teamsCount) == True or len(b) == maxlength) and len(zones) > 1:
            zones.remove('B')
        if (filterConfList(conf_name, c, teamsCount) == True or len(c) == maxlength) and len(zones) > 1:
            zones.remove('C')
        if (filterConfList(conf_name, d, teamsCount) == True or len(d) == maxlength) and len(zones) > 1:
            zones.remove('D')
        if (filterConfList(conf_name, e, teamsCount) == True or len(e) == maxlength) and len(zones) > 1:
            zones.remove('E')
        if (filterConfList(conf_name, f, teamsCount) == True or len(f) == maxlength) and len(zones) > 1:
            zones.remove('F')
        if (filterConfList(conf_name, g, teamsCount) == True or len(g) == maxlength) and len(zones) > 1:
            zones.remove('G')
        if (filterConfList(conf_name, h, teamsCount) == True or len(h) == maxlength) and len(zones) > 1:
            zones.remove('H')
        if len(zones) > 1:
            random.shuffle(zones)

        return zones[0]
    except:
        print('Error al generar sorteo')


def filterConfList(conf_name, list, count_teams):
    count_conf = 0
    for team in list:
        if conf_name == team['conf_name']:
            count_conf += 1
    if count_teams <= 8 and count_conf == 1:
        return True
    elif count_teams > 8 and count_conf == 2:
        return True
    return False


def countTeams(conf_name, teamList):
    count = 0
    for team in teamList:
        if conf_name == team['conf_name']:
            count += 1
    return count


def playoffDraw(teams):
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

    return pool1, pool2, pool3, pool4, pool5
