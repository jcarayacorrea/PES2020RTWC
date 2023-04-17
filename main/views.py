from django.http import JsonResponse
from django.shortcuts import render
from django.template.defaulttags import register

from utils import getTeamsJSON, getQualyPlaces, getRoundPlaces
from fixtures import getZoneData
from PESSimulator import simular_partido


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
    lenght = len(fixtureDict['teams']) + 1
    context['teams'] = zip(fixtureDict['teams'], range(1, lenght), placesList)

    return render(request, 'popups/standings/standings.html', context)


def sim_match(request, fixture, match, homeId, awayId, conf, round, zone):
    resultado = simular_partido(homeId, awayId)
    context = {}
    fixtureDict = getZoneData(zone, conf, round)
    context['fixture'] = fixtureDict['fixtures']
    context['conf'] = conf
    context['round'] = round
    context['zone'] = zone
    fixtures = {}
    match fixture:
        case 1:
            fixtures = {'fixture1': saveMatchObj(match, resultado)}
        case 2:
            fixtures = {'fixture2': saveMatchObj(match, resultado)}
        case 3:
            fixtures = {'fixture3': saveMatchObj(match, resultado)}
        case 4:
            fixtures = {'fixture4': saveMatchObj(match, resultado)}
        case 5:
            fixtures = {'fixture5': saveMatchObj(match, resultado)}
        case 6:
            fixtures = {'fixture6': saveMatchObj(match, resultado)}
        case 7:
            fixtures = {'fixture7': saveMatchObj(match, resultado)}
        case 8:
            fixtures = {'fixture8': saveMatchObj(match, resultado)}
        case 9:
            fixtures = {'fixture9': saveMatchObj(match, resultado)}
        case _:
            fixtures = {'fixture10': saveMatchObj(match, resultado)}

    return render(request, 'popups/fixtures/fixture.html', context)


@register.filter
def getItem(dict, key):
    return dict.get(key)


def saveMatchObj(match, resultado):
    matchDetail = {"match1": {"homeTeam": {"goals": None, "result": False},
                              "awayTeam": {"goals": None, "result": False}},
                   "match2": {"homeTeam": {"goals": None, "result": False},
                              "awayTeam": {"goals": None, "result": False}}}
    match match:
        case 1:
            matchDetail['match1']['homeTeam']['goals'] = resultado['local']
            matchDetail['match1']['awayTeam']['goals'] = resultado['visita']
            if resultado['local'] > resultado['visita']:
                matchDetail['match1']['homeTeam']['result'] = True
                matchDetail['match1']['awayTeam']['result'] = False
            else:
                matchDetail['match1']['homeTeam']['result'] = False
                matchDetail['match1']['awayTeam']['result'] = True
        case 2:
            matchDetail['match2']['homeTeam']['goals'] = resultado['local']
            matchDetail['match2']['awayTeam']['goals'] = resultado['visita']
            if resultado['local'] > resultado['visita']:
                matchDetail['match2']['homeTeam']['result'] = True
                matchDetail['match2']['awayTeam']['result'] = False
            else:
                matchDetail['match2']['homeTeam']['result'] = False
                matchDetail['match2']['awayTeam']['result'] = True
    return matchDetail
