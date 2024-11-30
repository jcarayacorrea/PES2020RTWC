import random

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.defaulttags import register
from fixtures import createPlayOffMatches, getZoneData
from utils import getTeamsMainDraw, getTeamsPlayoff
from functools import reduce


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
        zone1, zone2, zone3,  = playoffDraw(getTeamsPlayoff())
        random.shuffle(zone1)
        random.shuffle(zone2)
        random.shuffle(zone3)

        createPlayOffMatches(getTeamsPlayoff(), zone1, zone2, zone3)
        playoffData = getZoneData('P', 'FIFA', 'playoff')
        context['fixture'] = playoffData['fixtures']

        return render(request, 'worldcup/playoff.html', context)


def draw(teams):
    groups = {
        'A': [],
        'B': [],
        'C': [],
        'D': [],
        'E': [],
        'F': [],
        'G': [],
        'H': []
    }
    pool1 = teams[0:8]
    pool2 = teams[8:16]
    pool3 = teams[16:24]
    pool4 = teams[24:32]
    random.shuffle(pool1)
    for key, team in zip(groups.keys(), pool1):
        groups.get(key).append(team)

    pools = [pool2, pool3, pool4]

    for pool, i in zip(pools, range(2, 5)):
        random.shuffle(pool)
        for team in pool:
            setTeamPosition(team, groups, i - 1, teamsCount=countTeams(team['conf_name'], getTeamsMainDraw()),
                            maxLength=i)
    return groups.get('A'), groups.get('B'), groups.get('C'), groups.get('D'), groups.get('E'), groups.get(
        'F'), groups.get('G'), groups.get('H')


def setTeamPosition(team, groups, position, teamsCount, maxLength):
    zones = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    for zone in zones.copy():
        if filterConfList(team['conf_name'], groups.get(zone), teamsCount) == True or len(
                groups.get(zone)) == maxLength:
            zones.remove(zone)

    insertTeam(team, random.choice(zones), position, groups)


def filterConfList(conf_name, list, count_teams):
    count_conf = len([team for team in list if conf_name == team['conf_name']])
    if (count_teams <= 8 and count_conf == 1) or (count_teams > 8 and count_conf == 2):
        return True
    return False


def countTeams(conf_name, teamList):
    return len([team for team in teamList if conf_name == team['conf_name']])


def insertTeam(team, zone, pos, groups):
    match (zone):
        case 'A':
            groups.get('A').insert(pos, team)
        case 'B':
            groups.get('B').insert(pos, team)
        case 'C':
            groups.get('C').insert(pos, team)
        case 'D':
            groups.get('D').insert(pos, team)
        case 'E':
            groups.get('E').insert(pos, team)
        case 'F':
            groups.get('F').insert(pos, team)
        case 'G':
            groups.get('G').insert(pos, team)
        case 'H':
            groups.get('H').insert(pos, team)


def playoffDraw(teams):
    pool1 = teams[0:6]
    pool2 = teams[6:12]
    pool3 = teams[12:18]


    random.shuffle(pool1)
    random.shuffle(pool2)
    random.shuffle(pool3)


    return pool1, pool2, pool3


@register.filter
def teamsByConf(dict, conf):
    return countTeams(conf, dict);
