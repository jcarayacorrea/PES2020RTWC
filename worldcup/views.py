import random

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.defaulttags import register

from Global_Variables import GROUP_RANGE, GROUP_KEYS
from fixtures import createPlayOffMatches, getZoneData
from utils import getTeamsMainDraw, getTeamsPlayoff
from functools import reduce

GROUP_COUNT = len(GROUP_KEYS)
MIN_TEAMS = 1
MAX_TEAMS = 2


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


def shuffle_teams_and_assign_to_context(groups):
    context = {}
    for i, zone_key in enumerate(GROUP_KEYS):
        zone_teams = groups[zone_key]
        random.shuffle(zone_teams)
        context[f'zone{zone_key}'] = zone_teams
    return context


def draw_main_button(request):
    if request.method == 'GET':
        confederations = ['CONMEBOL', 'UEFA', 'CONCACAF', 'OFC', 'CAF', 'AFC']
        teams = getTeamsMainDraw()
        context = {'teams': teams, 'confederations': confederations}
        
        # Iterative retry instead of recursion to avoid potential RecursionError
        max_attempts = 100
        for _ in range(max_attempts):
            try:
                groups = draw(teams)
                zone_context = shuffle_teams_and_assign_to_context(groups)
                context.update(zone_context)
                break
            except (ValueError, IndexError):
                continue
        else:
            # If it fails after max_attempts, we should probably handle it gracefully
            return HttpResponse("Failed to generate a valid draw after multiple attempts", status=500)
            
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
    groups = {key: [] for key in GROUP_KEYS}
    
    # Pool 1: Seeded teams (first 8)
    for key, team in zip(GROUP_KEYS, shuffleArray(teams[0:8])):
        groups[key].append(team)

    # Pools 2, 3, 4 (teams 8-15, 16-23, 24-31)
    pools = [teams[8:16], teams[16:24], teams[24:32]]
    for pool_idx, pool in enumerate(pools):
        shuffled_pool = shuffleArray(pool)
        max_length = pool_idx + 2
        for team in shuffled_pool:
            setTeamPosition(
                team, 
                groups, 
                teams_count=countTeams(team['conf_name'], teams),
                max_length=max_length
            )
            
    return groups


def setTeamPosition(team, groups, teams_count, max_length):
    available_zones = []
    for zone in GROUP_KEYS:
        is_conf_limit_reached = filterConfList(team['conf_name'], groups[zone], teams_count)
        is_group_full = len(groups[zone]) == max_length
        
        if not is_conf_limit_reached and not is_group_full:
            available_zones.append(zone)
            
    if not available_zones:
        # Raising an error to trigger a retry in draw_main_button
        raise ValueError(f"No available zones for team {team.get('name')} from {team['conf_name']}")
        
    chosen_zone = random.choice(available_zones)
    groups[chosen_zone].append(team)


def filterConfList(conf_name, group_list, total_teams_in_conf):
    count_in_group = len([team for team in group_list if team['conf_name'] == conf_name])
    if total_teams_in_conf <= GROUP_COUNT:
        return count_in_group >= MIN_TEAMS
    else:
        return count_in_group >= MAX_TEAMS


def countTeams(conf_name, teamList):
    return len([team for team in teamList if conf_name == team['conf_name']])


def insertTeam(team, zone, groups):
    groups.get(zone).append(team)


@register.filter
def teamsByConf(dict, conf):
    return countTeams(conf, dict)


def shuffleArray(array):
    random.shuffle(array)
    return array
