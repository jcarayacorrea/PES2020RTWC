import random

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.defaulttags import register
from fixtures import createPlayOffMatches, getZoneData
from utils import getTeamsMainDraw, getTeamsPlayoff
from functools import reduce


# Create your views here.
def maindraw(request):
    teams = getTeamsMainDraw()
    confederations = ['CONMEBOL', 'UEFA', 'CONCACAF', 'OFC', 'CAF', 'AFC']
    context = {'teams': teams, 'confederations': confederations}

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
    for i, zone in enumerate(zones):
        random.shuffle(zone)
        context[f'zone{chr(65 + i)}'] = zone
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


def assign_teams_to_groups(teams, groups):
    # Assigns a list of teams to groups
    pool = teams
    random.shuffle(pool)
    for key, team in zip(groups.keys(), pool):
        groups.get(key).append(team)
    return groups


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

    # manually creating pools and assigning them to groups
    for i in range(4):
        start_index = i * 8
        end_index = start_index + 8
        pool_teams = teams[start_index:end_index]
        groups = assign_teams_to_groups(pool_teams, groups)

    return groups


def set_team_position(team, groups, position, teams_count, max_length):
    all_zones = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    valid_zones = [zone for zone in all_zones if not (
            filter_conf_list(team['conf_name'], groups.get(zone), teams_count) or len(
        groups.get(zone)) == max_length)]
    insertTeam(team, random.choice(valid_zones), position, groups)


def is_valid_team_count(count_teams, count_conf):
    return (count_teams <= 8 and count_conf == 1) or (count_teams > 8 and count_conf == 2)


def filter_conf_list(conf_name, team_list, count_teams):
    count_conf = len([team for team in team_list if conf_name == team['conf_name']])
    return is_valid_team_count(count_teams, count_conf)


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
