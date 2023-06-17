from utils import db_conexion


def createFixture(teams, homeAway, zone, conf, round):
    fixtures = {}
    match len(teams):
        case 3:
            if homeAway == True:
                fixtures = {"fixture1": {"match1": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False},"played": False},
                                         "byeTeam": teams[2]},
                            "fixture2": {"match1": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[0], "goals": None, "result": False},"played": False},
                                         "byeTeam": teams[1]},
                            "fixture3": {"match1": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False},"played": False},
                                         "byeTeam": teams[0]},
                            "fixture4": {"match1": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[0], "goals": None, "result": False},"played": False},
                                         "byeTeam": teams[2]},
                            "fixture5": {"match1": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False},"played": False},
                                         "byeTeam": teams[1]},
                            "fixture6": {"match1": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False},"played": False},
                                         "byeTeam": teams[0]},
                            }

            else:
                fixtures = {"fixture1": {"match1": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False},"played": False},
                                         "byeTeam": teams[2]},
                            "fixture2": {"match1": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[0], "goals": None, "result": False},"played": False},
                                         "byeTeam": teams[1]},
                            "fixture3": {"match1": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False},"played": False},
                                         "byeTeam": teams[0]},
                            }

        case 4:
            if homeAway == True:
                fixtures = {"fixture1": {"match1": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False},"played": False},
                                         "match2": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[3], "goals": None, "result": False},"played": False},
                                         "byeTeam": None},
                            "fixture2": {"match1": {"homeTeam": {"team": teams[3], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[0], "goals": None, "result": False},"played": False},
                                         "match2": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False},"played": False},
                                         "byeTeam": None},
                            "fixture3": {"match1": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[3], "goals": None, "result": False},"played": False},
                                         "match2": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False},"played": False},
                                         "byeTeam": None},
                            "fixture4": {"match1": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[0], "goals": None, "result": False},"played": False},
                                         "match2": {"homeTeam": {"team": teams[3], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False},"played": False},
                                         "byeTeam": None},
                            "fixture5": {"match1": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[3], "goals": None, "result": False},"played": False},
                                         "match2": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False},"played": False},
                                         "byeTeam": None},
                            "fixture6": {"match1": {"homeTeam": {"team": teams[3], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False},"played": False},
                                         "match2": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[0], "goals": None, "result": False},"played": False},
                                         "byeTeam": None}
                            }

            else:
                fixtures = {"fixture1": {"match1": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False},"played": False},
                                         "match2": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[3], "goals": None, "result": False},"played": False},
                                         "byeTeam": None},
                            "fixture2": {"match1": {"homeTeam": {"team": teams[3], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[0], "goals": None, "result": False},"played": False},
                                         "match2": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False},"played": False},
                                         "byeTeam": None},
                            "fixture3": {"match1": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[3], "goals": None, "result": False},"played": False},
                                         "match2": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False},"played": False},
                                         "byeTeam": None}
                            }
        case 5:
            if homeAway == True:
                fixtures = {"fixture1": {"match1": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False},"played": False},
                                         "match2": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[3], "goals": None, "result": False},"played": False},
                                         "byeTeam": teams[4]},
                            "fixture2": {"match1": {"homeTeam": {"team": teams[4], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[0], "goals": None, "result": False},"played": False},
                                         "match2": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False},"played": False},
                                         "byeTeam": teams[3]},
                            "fixture3": {"match1": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[4], "goals": None, "result": False},"played": False},
                                         "match2": {"homeTeam": {"team": teams[3], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[0], "goals": None, "result": False},"played": False},
                                         "byeTeam": teams[2]},
                            "fixture4": {"match1": {"homeTeam": {"team": teams[3], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False},"played": False},
                                         "match2": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[4], "goals": None, "result": False},"played": False},
                                         "byeTeam": teams[0]},
                            "fixture5": {"match1": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False},"played": False},
                                         "match2": {"homeTeam": {"team": teams[4], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[3], "goals": None, "result": False},"played": False},
                                         "byeTeam": teams[1]},
                            "fixture6": {"match1": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[0], "goals": None, "result": False},"played": False},
                                         "match2": {"homeTeam": {"team": teams[3], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False},"played": False},
                                         "byeTeam": teams[4]},
                            "fixture7": {"match1": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[4], "goals": None, "result": False},"played": False},
                                         "match2": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False},"played": False},
                                         "byeTeam": teams[3]},
                            "fixture8": {"match1": {"homeTeam": {"team": teams[4], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False},"played": False},
                                         "match2": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[3], "goals": None, "result": False},"played": False},
                                         "byeTeam": teams[2]},
                            "fixture9": {"match1": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[3], "goals": None, "result": False},"played": False},
                                         "match2": {"homeTeam": {"team": teams[4], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False},"played": False},
                                         "byeTeam": teams[0]},
                            "fixture10": {"match1": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                     "awayTeam": {"team": teams[0], "goals": None, "result": False},"played": False},
                                          "match2": {"homeTeam": {"team": teams[3], "goals": None, "result": False},
                                                     "awayTeam": {"team": teams[4], "goals": None, "result": False},"played": False},
                                          "byeTeam": teams[1]}

                            }

            else:
                fixtures = {"fixture1": {"match1": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False},"played": False},
                                         "match2": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[3], "goals": None, "result": False},"played": False},
                                         "byeTeam": teams[4]},
                            "fixture2": {"match1": {"homeTeam": {"team": teams[4], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[0], "goals": None, "result": False},"played": False},
                                         "match2": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False},"played": False},
                                         "byeTeam": teams[3]},
                            "fixture3": {"match1": {"homeTeam": {"team": teams[1], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[4], "goals": None, "result": False},"played": False},
                                         "match2": {"homeTeam": {"team": teams[3], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[0], "goals": None, "result": False},"played": False},
                                         "byeTeam": teams[2]},
                            "fixture4": {"match1": {"homeTeam": {"team": teams[3], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[1], "goals": None, "result": False},"played": False},
                                         "match2": {"homeTeam": {"team": teams[2], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[4], "goals": None, "result": False},"played": False},
                                         "byeTeam": teams[0]},
                            "fixture5": {"match1": {"homeTeam": {"team": teams[0], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[2], "goals": None, "result": False},"played": False},
                                         "match2": {"homeTeam": {"team": teams[4], "goals": None, "result": False},
                                                    "awayTeam": {"team": teams[3], "goals": None, "result": False},"played": False},
                                         "byeTeam": teams[1]},

                            }
    updateFixture(teams, fixtures, zone, conf, round)


def updateFixture(teams, fixtures, zone, conf, round):
    db = db_conexion()
    db.get_collection('Fixtures').update_one({'$and': [{'conf_name': conf}, {'zone': zone}, {'round': round}]},
                                             {'$set': {
                                                 'teams': teams,
                                                 'fixtures': fixtures
                                             }})


def getZoneData(zone, conf, round):
    db = db_conexion()
    cursor = db.get_collection('Fixtures').find(
        {'$and': [{'conf_name': conf}, {'zone': zone}, {'round': round}]})
    listData = list(cursor)
    return listData[0]


def createPlayOffMatches(teamList, seeds, pool1, pool2, pool3, pool4):
    firstPhasefixture = {"first": {
        "match1": {"homeTeam": {"team": pool3[0], "goals": None, "penalties": None},
                   "awayTeam": {"team": pool4[0], "goals": None, "penalties": None}, "result": False,
                   "played": False},
        "match2": {"homeTeam": {"team": pool3[1], "goals": None, "penalties": None},
                   "awayTeam": {"team": pool4[1], "goals": None, "penalties": None}, "result": False,
                   "played": False},
        "match3": {"homeTeam": {"team": pool3[2], "goals": None, "penalties": None},
                   "awayTeam": {"team": pool4[2], "goals": None, "penalties": None}, "result": False,
                   "played": False},
        "match4": {"homeTeam": {"team": pool3[3], "goals": None, "penalties": None},
                   "awayTeam": {"team": pool4[3], "goals": None, "penalties": None}, "result": False,
                   "played": False}
    },
        "final": {
            "match1": {"homeTeam": {"team": seeds[0], "goals": None, "penalties": None},
                       "awayTeam": {"team": None, "goals": None, "penalties": None}, "result": False,
                       "played": False},
            "match2": {"homeTeam": {"team": seeds[1], "goals": None, "penalties": None},
                       "awayTeam": {"team": None, "goals": None, "penalties": None}, "result": False,
                       "played": False},
            "match3": {"homeTeam": {"team": seeds[2], "goals": None, "penalties": None},
                       "awayTeam": {"team": None, "goals": None, "penalties": None}, "result": False,
                       "played": False},
            "match4": {"homeTeam": {"team": seeds[3], "goals": None, "penalties": None},
                       "awayTeam": {"team": None, "goals": None, "penalties": None}, "result": False,
                       "played": False},
            "match5": {"homeTeam": {"team": pool1[0], "goals": None, "penalties": None},
                       "awayTeam": {"team": pool2[0], "goals": None, "penalties": None}, "result": False,
                       "played": False},
            "match6": {"homeTeam": {"team": pool1[1], "goals": None, "penalties": None},
                       "awayTeam": {"team": pool2[1], "goals": None, "penalties": None}, "result": False,
                       "played": False},
            "match7": {"homeTeam": {"team": pool1[2], "goals": None, "penalties": None},
                       "awayTeam": {"team": pool2[2], "goals": None, "penalties": None}, "result": False,
                       "played": False},
            "match8": {"homeTeam": {"team": pool1[3], "goals": None, "penalties": None},
                       "awayTeam": {"team": pool2[3], "goals": None, "penalties": None}, "result": False,
                       "played": False}
        }

    }
    updateFixture(teamList, firstPhasefixture, 'P', 'FIFA', 'playoff')
