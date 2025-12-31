from utils import db_conexion

def create_match(home_team, away_team):
    return {
        "homeTeam": {"team": home_team, "goals": None, "result": False},
        "awayTeam": {"team": away_team, "goals": None, "result": False},
        "played": False
    }


def create_fixture(teams, home_away_indicator, zone, conf, round):
    matches_schedule = {}
    match len(teams):
        case 3:
            matches_schedule = {
                "fixture1": {"match1": create_match(teams[0], teams[1]), "byeTeam": teams[2]},
                "fixture2": {"match1": create_match(teams[2], teams[0]), "byeTeam": teams[1]},
                "fixture3": {"match1": create_match(teams[1], teams[2]), "byeTeam": teams[0]},
                "fixture4": {"match1": create_match(teams[1], teams[0]), "byeTeam": teams[2]},
                "fixture5": {"match1": create_match(teams[0], teams[2]), "byeTeam": teams[1]},
                "fixture6": {"match1": create_match(teams[2], teams[1]), "byeTeam": teams[0]},
            } if home_away_indicator else {
                "fixture1": {"match1": create_match(teams[0], teams[1]), "byeTeam": teams[2]},
                "fixture2": {"match1": create_match(teams[2], teams[0]), "byeTeam": teams[1]},
                "fixture3": {"match1": create_match(teams[1], teams[2]), "byeTeam": teams[0]},
            }
        case 4:
            matches_schedule = {
                "fixture1": {"match1": create_match(teams[0], teams[1]), "match2": create_match(teams[2], teams[3]),
                             "byeTeam": None},
                "fixture2": {"match1": create_match(teams[3], teams[0]), "match2": create_match(teams[1], teams[2]),
                             "byeTeam": None},
                "fixture3": {"match1": create_match(teams[1], teams[3]), "match2": create_match(teams[0], teams[2]),
                             "byeTeam": None},
                "fixture4": {"match1": create_match(teams[1], teams[0]), "match2": create_match(teams[3], teams[2]),
                             "byeTeam": None},
                "fixture5": {"match1": create_match(teams[0], teams[3]), "match2": create_match(teams[2], teams[1]),
                             "byeTeam": None},
                "fixture6": {"match1": create_match(teams[3], teams[1]), "match2": create_match(teams[2], teams[0]),
                             "byeTeam": None},
            } if home_away_indicator else {
                "fixture1": {"match1": create_match(teams[0], teams[1]), "match2": create_match(teams[2], teams[3]),
                             "byeTeam": None},
                "fixture2": {"match1": create_match(teams[3], teams[0]), "match2": create_match(teams[1], teams[2]),
                             "byeTeam": None},
                "fixture3": {"match1": create_match(teams[1], teams[3]), "match2": create_match(teams[0], teams[2]),
                             "byeTeam": None}
            }
        case 5:
            matches_schedule = {
                "fixture1": {"match1": create_match(teams[0], teams[1]), "match2": create_match(teams[2], teams[3]),
                             "byeTeam": teams[4]},
                "fixture2": {"match1": create_match(teams[4], teams[0]), "match2": create_match(teams[1], teams[2]),
                             "byeTeam": teams[3]},
                "fixture3": {"match1": create_match(teams[1], teams[4]), "match2": create_match(teams[3], teams[0]),
                             "byeTeam": teams[2]},
                "fixture4": {"match1": create_match(teams[3], teams[1]), "match2": create_match(teams[2], teams[4]),
                             "byeTeam": teams[0]},
                "fixture5": {"match1": create_match(teams[0], teams[2]), "match2": create_match(teams[4], teams[3]),
                             "byeTeam": teams[1]},
                "fixture6": {"match1": create_match(teams[1], teams[0]), "match2": create_match(teams[3], teams[2]),
                             "byeTeam": teams[4]},
                "fixture7": {"match1": create_match(teams[0], teams[4]), "match2": create_match(teams[2], teams[1]),
                             "byeTeam": teams[3]},
                "fixture8": {"match1": create_match(teams[4], teams[1]), "match2": create_match(teams[0], teams[3]),
                             "byeTeam": teams[2]},
                "fixture9": {"match1": create_match(teams[1], teams[3]), "match2": create_match(teams[4], teams[2]),
                             "byeTeam": teams[0]},
                "fixture10": {"match1": create_match(teams[2], teams[0]), "match2": create_match(teams[3], teams[4]),
                              "byeTeam": teams[1]},
            } if home_away_indicator else {
                "fixture1": {"match1": create_match(teams[0], teams[1]), "match2": create_match(teams[2], teams[3]),
                             "byeTeam": teams[4]},
                "fixture2": {"match1": create_match(teams[4], teams[0]), "match2": create_match(teams[1], teams[2]),
                             "byeTeam": teams[3]},
                "fixture3": {"match1": create_match(teams[1], teams[4]), "match2": create_match(teams[3], teams[0]),
                             "byeTeam": teams[2]},
                "fixture4": {"match1": create_match(teams[3], teams[1]), "match2": create_match(teams[2], teams[4]),
                             "byeTeam": teams[0]},
                "fixture5": {"match1": create_match(teams[0], teams[2]), "match2": create_match(teams[4], teams[3]),
                             "byeTeam": teams[1]},
            }
    updateFixture(teams, matches_schedule, zone, conf, round)



def updateFixture(teams, fixtures, zone, conf, round):
    db = db_conexion()
    db.get_collection('Fixtures').update_one({'$and': [{'conf': conf}, {'zone': zone}, {'round': round}]},
                                             {'$set': {
                                                 'teams': teams,
                                                 'fixtures': fixtures
                                             }})


def getZoneData(zone, conf, round):
    db = db_conexion()
    cursor = db.get_collection('Fixtures').find(
        {'$and': [{'conf': conf}, {'zone': zone}, {'round': round}]})
    listData = list(cursor)
    return listData[0]


def create_match(team1, team2):
    """Create a match dictionary object given two team names."""
    return {
        "homeTeam": {"team": team1, "goals": None, "penalties": None},
        "awayTeam": {"team": team2, "goals": None, "penalties": None},
        "result": False,
        "played": False
    }


def createPlayOffMatches(teamList, seeds, pool1, pool2):
    # defining initial match structure
    match_structure = {"first": {}, "final": {}}

    # loop through the elements of pool1 and pool2 to create matches
    for i in range(6):
        match_name = f"match{i + 1}"
        match_structure["first"][match_name] = create_match(pool1[i], pool2[i])
        match_structure["final"][match_name] = create_match(seeds[i], None)

    updateFixture(teamList, match_structure, 'P', 'FIFA', 'playoff')

def createPlayOffMatchesUEFA(teamList, pool1, pool2):
    # defining initial match structure
    match_structure = { "euro": {}}

    # loop through the elements of pool1 and pool2 to create matches
    for i in range(4):
        match_name = f"match{i + 1}"
        match_structure["euro"][match_name] = create_match(pool1[i], pool2[i])


    updateFixture(teamList, match_structure, 'P', 'UEFA', 'playoff')
