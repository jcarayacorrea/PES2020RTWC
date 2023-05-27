from django.http import JsonResponse
from django.shortcuts import render
from django.template.defaulttags import register

from utils import getTeamsJSON, getQualyPlaces, getRoundPlaces, saveMatchResult, saveExtraTimeResult
from fixtures import getZoneData
from standings import getStandings
from MatchSimulator import simular_partido


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def teamListApi(request):
    if request.method == 'GET':
        data = getTeamsJSON()
        return JsonResponse(data, safe=False)


def fixtureZone(request, conf, round, zone):
    context = {}
    fixtureDict = getZoneData(zone, conf, round)
    context['fixture'] = fixtureDict['fixtures']
    context['conf'] = conf
    context['round'] = round
    context['zone'] = zone
    return render(request, 'popups/fixtures/fixture.html', context)


def standingsZone(request, conf, round, zone):
    context = {}
    fixtureDict = getZoneData(zone, conf, round)
    placesDict = getQualyPlaces(conf)
    placesList = getRoundPlaces(placesDict, round)
    standings = getStandings(conf, round, zone)
    lenght = len(standings) + 1
    context['teams'] = zip(standings, range(1, lenght), placesList)

    return render(request, 'popups/standings/standings.html', context)


def sim_match(request, fixture, match, homeId, awayId, conf, round, zone, extraTime=0):
    extra = False if extraTime == 0 else True
    context = {}
    resultado = simular_partido(homeId, awayId, extra)
    if extraTime == 0:
        saveMatchResult(fixture, match, resultado['local'], resultado['visita'], conf, round, zone)
    else:
        saveExtraTimeResult(fixture,match,resultado['local'], resultado['visita'],resultado['penales_local'], resultado['penales_visita'], conf, round, zone)
    fixtureDict = getZoneData(zone, conf, round)
    context['fixture'] = fixtureDict['fixtures']
    context['conf'] = conf
    context['round'] = round
    context['zone'] = zone

    return render(request, 'popups/fixtures/fixture.html', context)


@register.filter
def getItem(dict, key):
    return dict.get(key)
