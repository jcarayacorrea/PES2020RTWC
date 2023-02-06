from utils import db_conexion


def createFixture(teams, homeAway, zone, conf, round):
    fixtures = {}
    match len(teams):
        case 3:
            if homeAway == True:
                fixtures = {"fixture1": {"match1": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False}},
                                         "byeTeam": teams[2]},
                            "fixture2": {"match1": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[0], "goals": None, "result": False}},
                                         "byeTeam": teams[1]},
                            "fixture3": {"match1": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False}},
                                         "byeTeam": teams[0]},
                            "fixture4": {"match1": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[0], "goals": None, "result": False}},
                                         "byeTeam": teams[2]},
                            "fixture5": {"match1": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False}},
                                         "byeTeam": teams[1]},
                            "fixture6": {"match1": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False}},
                                         "byeTeam": teams[0]},
                            }

            else:
                fixtures = {"fixture1": {"match1": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False}},
                                         "byeTeam": teams[2]},
                            "fixture2": {"match1": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[0], "goals": None, "result": False}},
                                         "byeTeam": teams[1]},
                            "fixture3": {"match1": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False}},
                                         "byeTeam": teams[0]},
                            }

        case 4:
            if homeAway == True:
                fixtures = {"fixture1": {"match1": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False}},
                                         "match2": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[3], "goals": None, "result": False}},
                                         "byeTeam": None},
                            "fixture2": {"match1": {"homeTeam": {"team": teams[3], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[0], "goals": None, "result": False}},
                                         "match2": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False}},
                                         "byeTeam": None},
                            "fixture3": {"match1": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[3], "goals": None, "result": False}},
                                         "match2": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False}},
                                         "byeTeam": None},
                            "fixture4": {"match1": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[0], "goals": None, "result": False}},
                                         "match2": {"homeTeam": {"team": teams[3], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False}},
                                         "byeTeam": None},
                            "fixture5": {"match1": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[3], "goals": None, "result": False}},
                                         "match2": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False}},
                                         "byeTeam": None},
                            "fixture6": {"match1": {"homeTeam": {"team": teams[3], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False}},
                                         "match2": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[0], "goals": None, "result": False}},
                                         "byeTeam": None}
                            }

            else:
                fixtures = {"fixture1": {"match1": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False}},
                                         "match2": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[3], "goals": None, "result": False}},
                                         "byeTeam": None},
                            "fixture2": {"match1": {"homeTeam": {"team": teams[3], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[0], "goals": None, "result": False}},
                                         "match2": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False}},
                                         "byeTeam": None},
                            "fixture3": {"match1": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[3], "goals": None, "result": False}},
                                         "match2": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False}},
                                         "byeTeam": None}
                            }
        case 5:
            if homeAway == True:
                fixtures = {"fixture1": {"match1": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False}},
                                         "match2": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[3], "goals": None, "result": False}},
                                         "byeTeam": teams[4]},
                            "fixture2": {"match1": {"homeTeam": {"team": teams[4], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[0], "goals": None, "result": False}},
                                         "match2": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False}},
                                         "byeTeam": teams[3]},
                            "fixture3": {"match1": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[4], "goals": None, "result": False}},
                                         "match2": {"homeTeam": {"team": teams[3], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[0], "goals": None, "result": False}},
                                         "byeTeam": teams[2]},
                            "fixture4": {"match1": {"homeTeam": {"team": teams[3], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False}},
                                         "match2": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[4], "goals": None, "result": False}},
                                         "byeTeam": teams[0]},
                            "fixture5": {"match1": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False}},
                                         "match2": {"homeTeam": {"team": teams[4], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[3], "goals": None, "result": False}},
                                         "byeTeam": teams[1]},
                            "fixture6": {"match1": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[0], "goals": None, "result": False}},
                                         "match2": {"homeTeam": {"team": teams[3], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False}},
                                         "byeTeam": teams[4]},
                            "fixture7": {"match1": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[4], "goals": None, "result": False}},
                                         "match2": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False}},
                                         "byeTeam": teams[3]},
                            "fixture8": {"match1": {"homeTeam": {"team": teams[4], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False}},
                                         "match2": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[3], "goals": None, "result": False}},
                                         "byeTeam": teams[2]},
                            "fixture9": {"match1": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[3], "goals": None, "result": False}},
                                         "match2": {"homeTeam": {"team": teams[4], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False}},
                                         "byeTeam": teams[0]},
                            "fixture10": {"match1": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                     "awayTeam": {"team": teams[0], "goals": None, "result": False}},
                                          "match2": {"homeTeam": {"team": teams[3], "goals": None, "result": False},
                                                     "awayTeam": {"team": teams[4], "goals": None, "result": False}},
                                          "byeTeam": teams[1]}

                            }

            else:
                fixtures = {"fixture1": {"match1": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False}},
                                         "match2": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[3], "goals": None, "result": False}},
                                         "byeTeam": teams[4]},
                            "fixture2": {"match1": {"homeTeam": {"team": teams[4], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[0], "goals": None, "result": False}},
                                         "match2": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False}},
                                         "byeTeam": teams[3]},
                            "fixture3": {"match1": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[4], "goals": None, "result": False}},
                                         "match2": {"homeTeam": {"team": teams[3], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[0], "goals": None, "result": False}},
                                         "byeTeam": teams[2]},
                            "fixture4": {"match1": {"homeTeam": {"team": teams[3], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False}},
                                         "match2": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[4], "goals": None, "result": False}},
                                         "byeTeam": teams[0]},
                            "fixture5": {"match1": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False}},
                                         "match2": {"homeTeam": {"team": teams[4], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[3], "goals": None, "result": False}},
                                         "byeTeam": teams[1]},

                            }
    updateFixture(teams,fixtures,zone,conf,round)

def updateFixture(teams,fixtures,zone,conf,round):
    db = db_conexion()
    db.get_collection('Fixtures').update_one({'$and': [{'conf_name': conf}, {'zone': zone},{'round':round}]},
    {'$set':{
        'teams': teams,
        'fixtures':fixtures
    }})

def getZoneData(zone,conf,round):
    db = db_conexion()
    cursor = db.get_collection('Fixtures').find(
        {'$and': [{'conf_name': conf}, {'zone': zone},{'round':round}]})
    listData = list(cursor)
    return listData[0]
