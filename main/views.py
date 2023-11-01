from django.http import JsonResponse, FileResponse
from django.shortcuts import render
from django.template.defaulttags import register
from django.contrib.staticfiles import finders
from html2image import Html2Image

from europa.views import firstround
from utils import getTeamsJSON, getQualyPlaces, getRoundPlaces, saveMatchResult, saveExtraTimeResult, getTeamById
from fixtures import getZoneData
from standings import getStandings
from MatchSimulator import simular_partido
from worldcup.views import playoff


# Create your views here.
def index(request):
    context = {}
    teams = getTeamsJSON()
    context['teams'] = teams
    return render(request, 'main/index.html', context)


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
        homeTeam = getTeamById(homeId)
        awayTeam = getTeamById(awayId)
        saveExtraTimeResult(fixture, match, resultado['local'], resultado['visita'],
                            resultado['penales_local'] if resultado.get('penales_local') else 0,
                            resultado['penales_visita'] if resultado.get('penales_visita') else 0, conf, round, zone,
                            homeTeam[0], awayTeam[0])
    fixtureDict = getZoneData(zone, conf, round)
    context['fixture'] = fixtureDict['fixtures']
    context['conf'] = conf
    context['round'] = round
    context['zone'] = zone

    if fixture == 'first' or fixture == 'final':
        return playoff(request)
    elif fixture == 'wildCard':
        return firstround(request)

    return render(request, 'popups/fixtures/fixture.html', context)


def downloadDraw(request):
    html2png = Html2Image()
    baseCSS = finders.find('base.scss')
    if request.method == 'POST':
        body = request.body
        return FileResponse(html2png.screenshot(html_str=body, css_file=baseCSS, save_as='worldCup.png'))


@register.filter
def getItem(dict, key):
    return dict.get(key)


@register.filter
def enableDrawButton(dict, length):
    if (len(dict) == length):
        return False
    return True


@register.simple_tag
def resultbghome(dict):
    if dict['played']:
            if dict['homeTeam']['result'] is True and dict['awayTeam']['result'] is False:
                return 'win'
            elif dict['homeTeam']['result'] is False and dict['awayTeam']['result'] is True:
                return 'lose'
            else:
                return 'draw'
    return 'non-played'



@register.simple_tag
def resultbgaway(dict):
    if dict['played']:
            if dict['homeTeam']['result'] is False and dict['awayTeam']['result'] is True:
                return 'win'
            elif dict['homeTeam']['result'] is True and dict['awayTeam']['result'] is False:
                return 'lose'
            else:
                return 'draw'
    return ''

@register.simple_tag
def rstonemtchhome(dict):
    if (dict['homeTeam']['goals'] > dict['awayTeam']['goals']) or (
             (dict['homeTeam']['penalties'] is not None) and
            (dict['homeTeam']['penalties'] > dict['awayTeam']['penalties'])):
        return 'win'
    else:
        return 'lose'

@register.simple_tag
def rstonemtchaway(dict):
    if (dict['homeTeam']['goals'] < dict['awayTeam']['goals']) or (
             (dict['homeTeam']['penalties'] is not None) and
            (dict['homeTeam']['penalties'] < dict['awayTeam']['penalties'])):
        return 'win'
    else:
        return 'lose'