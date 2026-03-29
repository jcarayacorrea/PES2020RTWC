from django import template
from typing import List, Dict, Any

register = template.Library()

@register.filter
def teams_by_conf(team_list: List[Dict[str, Any]], conf_name: str) -> int:
    """Counts teams belonging to a specific confederation."""
    return len([team for team in team_list if team['conf_name'] == conf_name])


@register.filter
def get_item(dictionary: Dict[Any, Any], key: Any) -> Any:
    """Gets an item from a dictionary."""
    return dictionary.get(key)


@register.filter
def enable_draw_button(team_list: List[Any], target_length: int) -> bool:
    """Determines if the draw button should be enabled."""
    return len(team_list) != target_length


@register.simple_tag
def result_bg_home(match_dict: Dict[str, Any]) -> str:
    """Determines the CSS class for the home team background based on the match result."""
    if match_dict.get('played'):
        home_res = match_dict['homeTeam'].get('result')
        away_res = match_dict['awayTeam'].get('result')
        if home_res is True and away_res is False:
            return 'win'
        elif home_res is False and away_res is True:
            return 'lose'
        else:
            return 'draw'
    return 'non-played'


@register.simple_tag
def result_bg_away(match_dict: Dict[str, Any]) -> str:
    """Determines the CSS class for the away team background based on the match result."""
    if match_dict.get('played'):
        home_res = match_dict['homeTeam'].get('result')
        away_res = match_dict['awayTeam'].get('result')
        if home_res is False and away_res is True:
            return 'win'
        elif home_res is True and away_res is False:
            return 'lose'
        else:
            return 'draw'
    return ''


@register.simple_tag
def result_one_match_home(match_dict: Dict[str, Any]) -> str:
    """Determines the result status for a single match (home team)."""
    if match_dict and match_dict.get('played'):
        h_goals = match_dict['homeTeam'].get('goals') or 0
        a_goals = match_dict['awayTeam'].get('goals') or 0
        h_pens = match_dict['homeTeam'].get('penalties')
        a_pens = match_dict['awayTeam'].get('penalties')
        
        if h_goals > a_goals or (h_pens is not None and a_pens is not None and h_pens > a_pens):
            return 'win'
        else:
            return 'lose'
    return ''


@register.simple_tag
def result_one_match_away(match_dict: Dict[str, Any]) -> str:
    """Determines the result status for a single match (away team)."""
    if match_dict and match_dict.get('played'):
        h_goals = match_dict['homeTeam'].get('goals') or 0
        a_goals = match_dict['awayTeam'].get('goals') or 0
        h_pens = match_dict['homeTeam'].get('penalties')
        a_pens = match_dict['awayTeam'].get('penalties')
        
        if h_goals < a_goals or (h_pens is not None and a_pens is not None and h_pens < a_pens):
            return 'win'
        else:
            return 'lose'
    return ''


@register.simple_tag
def concat_strings(*args: str) -> str:
    """Concatenates multiple strings."""
    return ''.join(args)
