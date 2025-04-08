import random

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from operator import itemgetter
from utils import getTeams, updateStage, getTeamsCopaAmerica, GROUP_RANGE

CONMEBOL_TEAMS = 2
CONCACAF_TEAMS = 2
REST_TEAMS = 10
POOL_TEAMS = 4


# Create your views here.
def teams(request):
    context = {}
    context['teams'] = getTeams(conf_name='CONMEBOL')
    return render(request, 'sudamerica/teamlist.html', context)


def copaAmerica(request):
    context = {}
    context['teams'] = getTeamsCopaAmerica()
    context['range'] = GROUP_RANGE[0:4]
    return render(request, 'sudamerica/copaamerica.html', context)


def updateProgress(request, id, stage):
    if request.method == 'POST':
        updateStage(id, stage)
    return redirect('sudamerica.finalround')


def copaAmericaButton(request):
    if request.method == 'GET':
        teams = getTeamsCopaAmerica()
        zones = copaAmericaDraw(teams)
        for zone in zones:
            random.shuffle(zone)
        context = {
            'teams': teams,
            'zoneA': zones[0],
            'zoneB': zones[1],
            'zoneC': zones[2],
            'zoneD': zones[3],
        }

        return render(request, 'sudamerica/copaamerica.html', context)


def extract_teams_by_federation(teams, federation):
    return [team for team in teams if team['conf_name'] == federation]


def create_zone(seed_list, *pools):
    return [seed_list.pop(),
            pools[0].pop(),
            pools[1].pop(),
            pools[2].pop()]


def shuffle_list(*args):
    for arg in args:
        random.shuffle(arg)


def copaAmericaDraw(teams):
    # Extract team lists by federation
    sudamerica = extract_teams_by_federation(teams, 'CONMEBOL')
    ncamerica = extract_teams_by_federation(teams, 'CONCACAF')

    # Create seed lists and rest of teams list
    sudSeed, ncSeed = sudamerica[:CONMEBOL_TEAMS], ncamerica[:CONCACAF_TEAMS]
    restTeams = sorted(sudamerica[CONMEBOL_TEAMS:REST_TEAMS] + ncamerica[CONCACAF_TEAMS:6],
                       key=itemgetter('fifa_nation_rank'))

    # Split restTeams into pools
    pool2, pool3, pool4 = [restTeams[i: i + POOL_TEAMS] for i in range(0, len(restTeams), POOL_TEAMS)]

    # Shuffle lists
    shuffle_list(sudSeed, ncSeed, pool2, pool3, pool4)

    # Creating zones
    zone1, zone2 = create_zone(sudSeed, pool2, pool3, pool4), create_zone(ncSeed, pool2, pool3, pool4)
    zone3, zone4 = create_zone(ncSeed, pool2, pool3, pool4), create_zone(sudSeed, pool2, pool3, pool4)

    return zone1, zone2, zone3, zone4
