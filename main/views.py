import string

from django.http import JsonResponse, FileResponse
from django.shortcuts import render
from django.template.defaulttags import register
from django.contrib.staticfiles import finders
from html2image import Html2Image

from europa.views import firstround
from utils import getTeamsJSON, getQualyPlaces, get_round_stages, saveMatchResult, saveExtraTimeResult, getTeamById
from fixtures import getZoneData
from standings import getStandings
from MatchSimulator import simulate_match
from worldcup.views import playoff
from oceania.views import finalround


# Create your views here.
def index(request):
    return render(request, 'main/index.html', {'teams': getTeamsJSON()})


def get_team_list(request):
    if request.method == 'GET':
        try:
            data = getTeamsJSON()
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse(data, safe=False)


def fixtureZone(request, conf, round, zone):
    fixtureDict = getZoneData(zone, conf, round)
    context = {
        'fixture': fixtureDict['fixtures'],
        'conf': conf,
        'round': round,
        'zone': zone
    }
    return render(request, 'popups/fixtures/fixture.html', context)


def bundle_teams(standings, placesList):
    length = len(standings) + 1
    bundled_teams = zip(standings, range(1, length), placesList)
    return bundled_teams


def standingsZone(request, conf, round, zone):
    """
    This function is responsible for assembling team standings for a given league round and zone.
    It fetches qualifying places, round stages, standings and bundles them together for rendering.

    :param request: HttpRequest object
    :param league: league configuration
    :param match_round: round of the match
    :param zone: zone for the standings
    """
    context = {}
    qualifying_places = getQualyPlaces(conf)
    round_stages = get_round_stages(qualifying_places, round)
    standings = getStandings(conf, round, zone)
    context['zip'] = bundle_teams(standings, round_stages)
    # Render the standings template with the provided context
    return render(request, 'popups/standings/standings.html', context)


def sim_match(request, fixture, match, homeid, awayid, conf, round, zone, extraTime=0, singleLoad=0):
    match_info = {'fixture': fixture, 'match': match, 'homeid': homeid, 'awayid': awayid};
    resultado = simulate_match(homeid, awayid, extraTime != 0)
    handle_match_results(match_info, resultado, conf, round, zone, extraTime != 0)
    if singleLoad == 1:
        return render_match_data(request, zone, conf, round, match_info["fixture"], match_info["match"])
    fixtureDict = getZoneData(zone, conf, round)
    return handle_match_configuration(request, fixtureDict, match_info["fixture"], conf, round, zone)


def handle_match_results(match_info, resultado, conf, round, zone, is_extra):
    if not is_extra:
        saveMatchResult(match_info["fixture"], match_info["match"], resultado['local'], resultado['visita'], conf,
                        round, zone)
    else:
        homeTeam = getTeamById(match_info["homeid"])
        awayTeam = getTeamById(match_info["awayid"])
        saveExtraTimeResult(match_info["fixture"], match_info["match"], resultado['local'], resultado['visita'],
                            resultado.get('penales_local', 0),
                            resultado.get('penales_visita', 0), conf, round, zone,
                            homeTeam[0], awayTeam[0])


def handle_match_configuration(request, fixture, conf, round, zone):
    responses = {
        'first': playoff,
        'final': playoff,
        'wildCard': firstround,
        'mainDraw': finalround
    }
    return responses.get(fixture, fixtureZone)(request, conf, round, zone)


def downloadDraw(request, namefile):
    html2png = Html2Image()
    baseCSS = finders.find('base.scss')
    if request.method == 'POST':
        body = request.body
        return FileResponse(html2png.screenshot(html_str=body, css_file=baseCSS, save_as=f'{namefile}.png'))


def render_match_data(request, zone_id, config, round_id, fixture_id, match_id):
    zone_data = getZoneData(zone_id, config, round_id)
    match_data = getMatchData(zone_data, fixture_id, match_id)
    context = {'match': match_data}
    return render(request, 'utils/fixture/match-card.html', context)


def getMatchData(fixtureDict, fixture, match):
    return fixtureDict['fixtures']['fixture' + str(fixture)]['match' + str(match)]


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
    if dict != '':
        if dict['played']:
            if (dict['homeTeam']['goals'] > dict['awayTeam']['goals']) or (
                    (dict['homeTeam']['penalties'] is not None) and
                    (dict['homeTeam']['penalties'] > dict['awayTeam']['penalties'])):
                return 'win'
            else:
                return 'lose'
    return ''


@register.simple_tag
def rstonemtchaway(dict):
    if dict != '':
        if dict['played']:
            if (dict['homeTeam']['goals'] < dict['awayTeam']['goals']) or (
                    (dict['homeTeam']['penalties'] is not None) and
                    (dict['homeTeam']['penalties'] < dict['awayTeam']['penalties'])):
                return 'win'
            else:
                return 'lose'
    return ''


@register.simple_tag
def concat_string(*args):
    return ''.join(args)
