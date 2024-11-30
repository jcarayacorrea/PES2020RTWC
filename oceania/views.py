import random

from django.shortcuts import render, redirect

from fixtures import getZoneData, createFixture
from utils import updateStage, getTeams, getTeamsFirstRound, getTeamsFinalRound, db_conexion, getTeamById


# Create your views here.
def finalround(request):
    context = {}
    context['teams'] = getTeamsFinalRound(conf_name='OFC')
    zone1 = getZoneData('A', 'OFC', 'final')
    zone2 = getZoneData('B', 'OFC', 'final')
    zoneMD = getZoneData('MD', 'OFC', 'final')
    if len(zone1['teams']) == 4:
        context['zone1'] = zone1['teams']
    if len(zone2['teams']) == 4:
        context['zone2'] = zone2['teams']


    context['fixture'] = zoneMD['fixtures']

    return render(request, 'oceania/finalround.html', context)


def firstround(request):
    context = {}
    context['teams'] = getTeamsFirstRound(conf_name='OFC')
    zone1 = getZoneData('A', 'OFC', 'first')
    if len(zone1['teams']) == 5:
        context['zone1'] = zone1['teams']
    return render(request, 'oceania/fstround.html', context)


def teams(request):
    context = {}
    context['teams'] = getTeams(conf_name='OFC')
    return render(request, 'oceania/teamlist.html', context)


def updateProgress(request, id, stage):
    if request.method == 'POST':
        updateStage(id, stage)
    return redirect('oceania.teams')


def firstRoundButton(request):
    if request.method == 'GET':
        context = {}
        context['teams'] = getTeamsFirstRound('OFC')
        zone1 = firstRoundDraw(getTeamsFirstRound('OFC'))

        createFixture(zone1, False, 'A', 'OFC', 'first')
        context['zone1'] = zone1

        return firstround(request)


def firstRoundDraw(teams):
    zone1 = teams

    return random.sample(zone1)


def finalRoundButton(request):
    if request.method == 'GET':
        context = {}
        context['teams'] = getTeamsFinalRound('OFC')
        zone1, zone2 = finalRoundDraw(getTeamsFinalRound('OFC'))

        createFixture(zone1, True, 'A', 'OFC', 'final')
        createFixture(zone2, True, 'B', 'OFC', 'final')
        context['zone1'] = zone1
        context['zone2'] = zone2

        return finalround(request)


def finalRoundDraw(teams):
    pool1 = [teams[0], teams[1]]
    pool2 = [teams[2], teams[3]]
    pool3 = [teams[4], teams[5]]
    pool4 = [teams[6], teams[7]]

    random.shuffle(pool1)
    random.shuffle(pool2)
    random.shuffle(pool3)
    random.shuffle(pool4)

    zone1 = [pool1[0], pool2[0], pool3[0], pool4[0]]
    zone2 = [pool1[1], pool2[1], pool3[1], pool4[1]]

    return random.shuffle(zone1), random.shuffle(zone2)

def setHomeFinalTeam(request):
    db = db_conexion()
    teamId = request.GET.get('home')
    team = getTeamById(teamId)
    db.get_collection('Fixtures').update_many({'$and': [{'conf': 'OFC'}, {'zone': 'MD'}, {'round': 'final'}]},
                                              {'$set': {
                                                  'fixtures.mainDraw.match1.played': False,
                                                  'fixtures.mainDraw.match1.homeTeam.team': team[0],
                                                  'fixtures.mainDraw.match1.homeTeam.goals': None,
                                                  'fixtures.mainDraw.match1.homeTeam.penalties': None
                                              }})
    return finalround(request)


def setAwayFinalTeam(request):
    db = db_conexion()
    teamId = request.GET.get('away')
    team = getTeamById(teamId)
    db.get_collection('Fixtures').update_one({'$and': [{'conf': 'OFC'}, {'zone': 'MD'}, {'round': 'final'}]},
                                             {'$set': {
                                                 'fixtures.mainDraw.match1.played': False,
                                                 'fixtures.mainDraw.match1.awayTeam.team': team[0],
                                                 'fixtures.mainDraw.match1.awayTeam.goals': None,
                                                 'fixtures.mainDraw.match1.awayTeam.penalties': None
                                             }})
    return finalround(request)