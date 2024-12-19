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
    context['confederations'] = ['CONMEBOL', 'UEFA', 'CONCACAF', 'OFC', 'CAF', 'AFC']
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
            zones = draw(getTeamsMainDraw())
        except:
            return maindrawButton(request)

        for i, zone in enumerate(zones):
            random.shuffle(zone)
            context[f'zone{chr(65 + i)}'] = zone

        return render(request, 'worldcup/maindraw.html', context)

def playoffButton(request):
    if request.method == 'GET':
        context = {}
        teams = getTeamsPlayoff()
        context['teams'] = teams

        zones = playoffDraw(teams)
        for zone in zones:
            random.shuffle(zone)

        createPlayOffMatches(teams, *zones)
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
    groups.get(zone).insert(pos, team)


def playoffDraw(teams):
    pools = []
    num_pools = 3
    teams_per_pool = 6

    for i in range(num_pools):
        start = i * teams_per_pool
        end = start + teams_per_pool
        pool = teams[start:end]
        random.shuffle(pool)
        pools.append(pool)

    return tuple(pools)


@register.filter
def teamsByConf(dict, conf):
    return countTeams(conf, dict)
