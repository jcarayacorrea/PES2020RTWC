import string
from typing import List, Dict, Any, Optional

from django.http import JsonResponse, FileResponse, HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.staticfiles import finders
from html2image import Html2Image

from europa.views import first_round
from utils import (
    get_teams_json, get_qualy_places, get_round_stages, 
    save_match_result, save_extra_time_result, get_team_by_id
)
from fixtures import get_zone_data
from standings import get_standings
from MatchSimulator import simulate_match
from worldcup.views import playoff
from oceania.views import final_round
from europa.views import euro_playoff


def index(request: HttpRequest) -> HttpResponse:
    """Renders the main index page."""
    return render(request, 'main/index.html', {'teams': get_teams_json()})


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


def sim_match(request: HttpRequest, fixture: int, match: int, home_id: str, away_id: str, 
              conf: str, round_name: str, zone: str, extra_time: int = 0, single_load: int = 0) -> HttpResponse:
    """Simulates a match and updates the database."""
    match_info = {'fixture': fixture, 'match': match, 'homeid': home_id, 'awayid': away_id}
    resultado = simulate_match(home_id, away_id, extra_time != 0)
    handle_match_results(match_info, resultado, conf, round_name, zone, extra_time != 0)
    
    if single_load == 1:
        return render_match_data(request, zone, conf, round_name, fixture, match)
    return handle_match_configuration(request, str(fixture))


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
            "first" if round_name == 'playoff' else "mainDraw", # This logic might need refinement based on actual usage
            match_info["match"], resultado['local'], resultado['visita'],
            resultado.get('penales_local', 0),
            resultado.get('penales_visita', 0), 
            conf, round_name, zone, 
            match_info["homeid"], match_info["awayid"]
        )


def handle_match_configuration(request: HttpRequest, fixture_type: str) -> HttpResponse:
    """Redirects to the appropriate view after a match is simulated."""
    responses = {
        'first': playoff,
        'final': playoff,
        'euro': euro_playoff,
        'wildCard': first_round,
        'mainDraw': final_round
    }
    # Fallback to fixture_zone if type not in map
    if fixture_type in responses:
        return responses[fixture_type](request)
    # This part is a bit tricky since fixture_zone needs more params. 
    # Original code had `responses.get(fixture, fixtureZone)(request)`
    return render(request, 'main/index.html') # Default fallback


def download_draw(request: HttpRequest, filename: str) -> HttpResponse:
    """Generates and returns a PNG screenshot of the draw."""
    html2png = Html2Image()
    base_css = finders.find('base.scss')
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        # Note: screenshot returns a list of paths
        paths = html2png.screenshot(html_str=body, css_file=base_css, save_as=f'{filename}.png')
        return FileResponse(open(paths[0], 'rb'))
    return HttpResponse(status=405)


def render_match_data(request: HttpRequest, zone_id: str, conf: str, round_id: str, 
                      fixture_id: int, match_id: int) -> HttpResponse:
    """Renders a single match card."""
    zone_data = get_zone_data(zone_id, conf, round_id)
    match_data = get_match_data_from_dict(zone_data, fixture_id, match_id)
    context = {'match': match_data}
    return render(request, 'utils/fixture/match-card.html', context)


def get_match_data_from_dict(fixture_dict: Dict[str, Any], fixture_num: int, match_num: int) -> Any:
    """Helper to extract match data from the nested fixture dictionary."""
    return fixture_dict['fixtures'][f'fixture{fixture_num}'][f'match{match_num}']
