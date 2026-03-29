from typing import List, Dict, Any
from operator import itemgetter
from fixtures import get_zone_data

def get_standings(conf: str, round_name: str, zone: str) -> List[Dict[str, Any]]:
    """Calculates and returns standings for a given zone."""
    fixture_data = get_zone_data(zone, conf, round_name)
    teams = fixture_data['teams']
    
    # Extract matches from the nested fixture structure
    all_matches = []
    fixtures_dict = fixture_data.get('fixtures', {})
    for fix_key in fixtures_dict:
        fix = fixtures_dict[fix_key]
        if isinstance(fix, dict):
            for match_key in ['match1', 'match2']:
                match_data = fix.get(match_key)
                if match_data:
                    all_matches.append(match_data)
                
    return create_standings(all_matches, teams)


def create_standings(matches: List[Dict[str, Any]], teams: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Processes matches to generate a sorted list of team standings."""
    standings = []
    for team in teams:
        team_id = team['nation_iso_code']
        stats = calculate_team_stats(team_id, matches)
        team_entry = {
            'team': team,
            'points': stats['points'],
            'matches': stats['played'],
            'favor': stats['goals_for'],
            'against': stats['goals_against'],
            'local': stats['goals_home'],
            'away': stats['goals_away'],
            'difference': stats['goals_for'] - stats['goals_against']
        }
        standings.append(team_entry)
        
    return sorted(standings, key=itemgetter('points', 'difference', 'favor', 'away'), reverse=True)


def calculate_team_stats(team_id: str, matches: List[Dict[str, Any]]) -> Dict[str, int]:
    """Aggregates match results for a specific team."""
    stats = {
        'points': 0,
        'played': 0,
        'goals_for': 0,
        'goals_against': 0,
        'goals_home': 0,
        'goals_away': 0
    }
    
    for match in matches:
        if not match.get('played'):
            continue
            
        home_team = match['homeTeam']
        away_team = match['awayTeam']
        
        # Guard against missing team info
        if not home_team.get('team') or not away_team.get('team'):
            continue
            
        home_id = home_team['team']['nation_iso_code']
        away_id = away_team['team']['nation_iso_code']
        
        h_goals = home_team.get('goals') or 0
        a_goals = away_team.get('goals') or 0
        
        if home_id == team_id:
            stats['played'] += 1
            stats['goals_for'] += h_goals
            stats['goals_against'] += a_goals
            stats['goals_home'] += h_goals
            
            if h_goals > a_goals:
                stats['points'] += 3
            elif h_goals == a_goals:
                stats['points'] += 1
                
        elif away_id == team_id:
            stats['played'] += 1
            stats['goals_for'] += a_goals
            stats['goals_against'] += h_goals
            stats['goals_away'] += a_goals
            
            if a_goals > h_goals:
                stats['points'] += 3
            elif a_goals == h_goals:
                stats['points'] += 1
                
    return stats
