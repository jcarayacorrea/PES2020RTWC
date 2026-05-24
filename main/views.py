from typing import List, Dict, Any

from django.http import JsonResponse, FileResponse, HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.staticfiles import finders
from html2image import Html2Image

from utils import (
    get_teams_json, get_qualy_places, get_round_stages,
    save_match_result, save_extra_time_result
)
from fixtures import get_zone_data
from standings import get_standings
from MatchSimulator import simulate_match
from worldcup.views import playoff as worldcup_playoff
from europa.views import euro_playoff, first_round as euro_first_round
from oceania.views import final_round as oceania_final_round


def index(request: HttpRequest) -> HttpResponse:
    """Renders the main index page."""
    return render(request, 'main/index.html', {'teams': get_teams_json()})


def flag_showcase(request: HttpRequest) -> HttpResponse:
    """Renders the flag display modes showcase page."""
    return render(request, 'main/flag_showcase.html')


def get_team_list(request: HttpRequest) -> JsonResponse:
    """Returns a JSON list of all teams."""
    if request.method == 'GET':
        try:
            data = get_teams_json()
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def fixture_zone(request: HttpRequest, conf: str, round_name: str, zone: str) -> HttpResponse:
    """Renders the fixture popup for a specific zone."""
    fixture_dict = get_zone_data(zone, conf, round_name)
    context = {
        'fixture': fixture_dict['fixtures'],
        'conf': conf,
        'round': round_name,
        'zone': zone
    }
    return render(request, 'popups/fixtures/fixture.html', context)


def bundle_teams(standings_list: List[Dict[str, Any]], places_list: List[Any]) -> Any:
    """Zips standings with their rank and qualification status."""
    length = len(standings_list) + 1
    return zip(standings_list, range(1, length), places_list)


def standings_zone(request: HttpRequest, conf: str, round_name: str, zone: str) -> HttpResponse:
    """Renders the standings popup for a specific zone."""
    qualifying_places = get_qualy_places(conf)
    round_stages = get_round_stages(qualifying_places, round_name)
    standings_list = get_standings(conf, round_name, zone)
    context = {'zip': bundle_teams(standings_list, round_stages)}
    return render(request, 'popups/standings/standings.html', context)


def sim_match(request: HttpRequest) -> HttpResponse:
    """Simulates a match via GET parameters and updates the database."""
    fixture = request.GET.get('fixture')
    match = int(request.GET.get('match', 0))
    home_id = request.GET.get('home', '')
    away_id = request.GET.get('away', '')
    conf = request.GET.get('conf', '')
    round_name = request.GET.get('round', '')
    zone = request.GET.get('zone', '')
    extra_time = request.GET.get('extra', '0') == '1'
    single_load = request.GET.get('load', '1') == '1'

    match_info = {'fixture': fixture, 'match': match, 'homeid': home_id, 'awayid': away_id}
    resultado = simulate_match(home_id, away_id, extra_time)
    handle_match_results(match_info, resultado, conf, round_name, zone, extra_time)

    if single_load:
        if fixture == 'mainDraw':
            return render_playoff_match_data(request, zone, conf, round_name, fixture, match)
        if extra_time:
            return render_playoff_match_data(request, zone, conf, round_name, fixture, match)
        return render_match_data(request, zone, conf, round_name, fixture, match)

    responses = {
        'first': worldcup_playoff,
        'final': worldcup_playoff,
        'euro': euro_playoff,
        'wildCard': euro_first_round,
        'mainDraw': oceania_final_round,
    }
    handler = responses.get(str(fixture))
    if handler:
        return handler(request)
    return render_match_data(request, zone, conf, round_name, fixture, match)


def handle_match_results(match_info: Dict[str, Any], resultado: Dict[str, Any],
                         conf: str, round_name: str, zone: str, is_extra: bool) -> None:
    """Saves match results to the database."""
    if not is_extra:
        save_match_result(
            match_info["fixture"], match_info["match"],
            resultado['local'], resultado['visita'],
            conf, round_name, zone
        )
    else:
        save_extra_time_result(
            match_info["fixture"],
            match_info["match"], resultado['local'], resultado['visita'],
            resultado.get('penales_local', 0),
            resultado.get('penales_visita', 0),
            conf, round_name, zone,
            match_info["homeid"], match_info["awayid"]
        )


def download_draw(request: HttpRequest) -> HttpResponse:
    """Generates and returns a PNG screenshot of the draw."""
    from uuid import uuid4
    if request.method != 'POST':
        return HttpResponse(status=405)
    html2png = Html2Image()
    base_css = finders.find('base.scss')
    if not base_css:
        return HttpResponse('base.scss not found', status=500)
    body = request.body.decode('utf-8')
    filename = f'draw_{uuid4().hex}'
    paths = html2png.screenshot(html_str=body, css_file=base_css, save_as=f'{filename}.png')
    return FileResponse(open(paths[0], 'rb'))


def render_match_data(request: HttpRequest, zone_id: str, conf: str, round_id: str, 
                      fixture_id: int, match_id: int) -> HttpResponse:
    """Renders a single match card for HTMX partial update."""
    zone_data = get_zone_data(zone_id, conf, round_id)
    match_data = get_match_data_from_dict(zone_data, fixture_id, match_id)
    context = {
        'match': match_data,
        'fixtureNum': fixture_id,
        'matchNum': match_id,
        'conf': conf,
        'round': round_id,
        'zone': zone_id,
        'delay': 0,
    }
    return render(request, 'utils/fixture/match-card.html', context)


def render_playoff_match_data(request: HttpRequest, zone_id: str, conf: str, round_id: str,
                              fixture_id: str, match_id: int) -> HttpResponse:
    """Renders a single playoff match card for JS fetch partial update."""
    zone_data = get_zone_data(zone_id, conf, round_id)
    match_data = get_match_data_from_dict(zone_data, fixture_id, match_id)
    context = {
        'match': match_data,
        'matchNum': match_id,
        'phase': fixture_id,
        'conf': conf,
        'home_empty': f'Team {match_id * 2 - 1}',
        'away_empty': f'Team {match_id * 2}',
        'zone': zone_id,
        'round': round_id,
    }
    return render(request, 'utils/playoff/match-card.html', context)


def get_match_data_from_dict(fixture_dict: Dict[str, Any], fixture_num: int, match_num: int) -> Any:
    """Helper to extract match data from the nested fixture dictionary."""
    fixtures = fixture_dict['fixtures']
    key = f'fixture{fixture_num}' if str(fixture_num).isdigit() else str(fixture_num)
    return fixtures[key][f'match{match_num}']
