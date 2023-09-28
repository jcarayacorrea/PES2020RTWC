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
            print("Intentando nuevamente....")
            return maindrawButton(request)

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
    pool1 = teams[0:8]
    pool2 = teams[8:16]
    pool3 = teams[16:24]
    pool4 = teams[24:32]
    random.shuffle(pool1)
    zoneA = [pool1[0]]
    zoneB = [pool1[1]]
    zoneC = [pool1[2]]
    zoneD = [pool1[3]]
    zoneE = [pool1[4]]
    zoneF = [pool1[5]]
    zoneG = [pool1[6]]
    zoneH = [pool1[7]]

    for i in range(2, 5):
        match (i):
            case 2:
                random.shuffle(pool2)
                for team in pool2:
                    setTeamPosition(team, zoneA, zoneB, zoneC, zoneD, zoneE, zoneF, zoneG, zoneH, i - 1,
                                    teamsCount=countTeams(team['conf_name'], getTeamsMainDraw()), maxLength=i)
            case 3:
                random.shuffle(pool3)
                for team in pool3:
                    setTeamPosition(team, zoneA, zoneB, zoneC, zoneD, zoneE, zoneF, zoneG, zoneH, i - 1,
                                    teamsCount=countTeams(team['conf_name'], getTeamsMainDraw()), maxLength=i)
            case 4:
                random.shuffle(pool4)
                for team in pool4:
                    setTeamPosition(team, zoneA, zoneB, zoneC, zoneD, zoneE, zoneF, zoneG, zoneH, i - 1,
                                    teamsCount=countTeams(team['conf_name'], getTeamsMainDraw()), maxLength=i)

    return zoneA, zoneB, zoneC, zoneD, zoneE, zoneF, zoneG, zoneH


def setTeamPosition(team, a, b, c, d, e, f, g, h, position, teamsCount, maxLength):
    zones = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    if filterConfList(team['conf_name'], a, teamsCount) == True or len(a) == maxLength:
        zones.remove('A')
    if filterConfList(team['conf_name'], b, teamsCount) == True or len(b) == maxLength:
        zones.remove('B')
    if filterConfList(team['conf_name'], c, teamsCount) == True or len(c) == maxLength:
        zones.remove('C')
    if filterConfList(team['conf_name'], d, teamsCount) == True or len(d) == maxLength:
        zones.remove('D')
    if filterConfList(team['conf_name'], e, teamsCount) == True or len(e) == maxLength:
        zones.remove('E')
    if filterConfList(team['conf_name'], f, teamsCount) == True or len(f) == maxLength:
        zones.remove('F')
    if filterConfList(team['conf_name'], g, teamsCount) == True or len(g) == maxLength:
        zones.remove('G')
    if filterConfList(team['conf_name'], h, teamsCount) == True or len(h) == maxLength:
        zones.remove('H')
    if len(zones) > 1:
        random.shuffle(zones)
    insertTeam(team, zones[0], position, a, b, c, d, e, f, g, h)


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


def insertTeam(team, zone, pos, a, b, c, d, e, f, g, h):
    match (zone):
        case 'A':
            a.insert(pos, team)
        case 'B':
            b.insert(pos, team)
        case 'C':
            c.insert(pos, team)
        case 'D':
            d.insert(pos, team)
        case 'E':
            e.insert(pos, team)
        case 'F':
            f.insert(pos, team)
        case 'G':
            g.insert(pos, team)
        case 'H':
            h.insert(pos, team)


def playoffDraw(teams):
    pool1 = [teams[0:3]]
    pool2 = [teams[4:7]]
    pool3 = [teams[8:11]]
    pool4 = [teams[12:15]]
    pool5 = [teams[16:19]]

    random.shuffle(pool1)
    random.shuffle(pool2)
    random.shuffle(pool3)
    random.shuffle(pool4)
    random.shuffle(pool5)

    return pool1, pool2, pool3, pool4, pool5
