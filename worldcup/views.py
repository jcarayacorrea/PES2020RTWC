import random

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.defaulttags import register

from Global_Variables import GROUP_RANGE, GROUP_KEYS
from fixtures import createPlayOffMatches, getZoneData
from utils import getTeamsMainDraw, getTeamsPlayoff
from functools import reduce


# Create your views here.
def maindraw(request):
    teams = getTeamsMainDraw()
    confederations = ['CONMEBOL', 'UEFA', 'CONCACAF', 'OFC', 'CAF', 'AFC']
    context = {'teams': teams, 'confederations': confederations, 'range': GROUP_RANGE[0:4]}

    return render(request, 'worldcup/maindraw.html', context)


def getPlayOffContextData():
    context = {}
    context['teams'] = getTeamsPlayoff()
    playoffData = getZoneData('P', 'FIFA', 'playoff')
    context['fixture'] = playoffData['fixtures']
    return context


def playoff(request):
    context = getPlayOffContextData()
    return render(request, 'worldcup/playoff.html', context)


def shuffle_teams_and_assign_to_context(zones):
    context = {}
    for i in range(len(zones)):
        random.shuffle(zones[i])
        context[f'zone{chr(65 + i)}'] = zones[i]
    return context


def draw_main_button(request):
    if request.method == 'GET':
        confederations = ['CONMEBOL', 'UEFA', 'CONCACAF', 'OFC', 'CAF', 'AFC']
        teams = getTeamsMainDraw()
        context = {'teams': teams, 'confederations': confederations}
        try:
            zones = draw(teams)
            zone_context = shuffle_teams_and_assign_to_context(zones)
            context.update(zone_context)
        except:
            return draw_main_button(request)
        return render(request, 'worldcup/maindraw.html', context)

def preparePlayoffData():
    teams = getTeamsPlayoff()
    zones = playoffDraw(teams)
    for zone in zones:
        random.shuffle(zone)
    createPlayOffMatches(teams, *zones)
    zone_identifier = 'P'
    conf = 'FIFA'
    round_type = 'playoff'
    playoffData = getZoneData(zone_identifier, conf, round_type)

    return teams, playoffData['fixtures']


def getPlayoffPage(request):
    if request.method == 'GET':
        playoffTeams, playoffFixtures = preparePlayoffData()
        context = {'teams': playoffTeams, 'fixture': playoffFixtures}
        return render(request, 'worldcup/playoff.html', context)





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
            setTeamPosition(team, groups, i - 1, teamsCount=countTeams(team['conf_name'], teams),
                            maxLength=i)
    return groups.get('A'), groups.get('B'), groups.get('C'), groups.get('D'), groups.get('E'), groups.get(
        'F'), groups.get('G'), groups.get('H')


def setTeamPosition(team, groups, position, teamsCount, maxLength):
    zones = GROUP_KEYS.copy()
    for zone in GROUP_KEYS:
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




@register.filter
def teamsByConf(dict, conf):
    return countTeams(conf, dict)
