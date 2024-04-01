from bson.json_util import dumps
from pymongo import MongoClient


def db_conexion():
    client = MongoClient(host='192.168.1.101',
                         port=27017,
                         username='admin',
                         password='mongo')
    db = client['pesrtwc']
    return db


def getTeams(conf_name):
    db = db_conexion()
    cursor = db.get_collection('Teams').find({'conf_name': conf_name}).sort('fifa_nation_rank', 1)
    listData = list(cursor)
    return listData


def getTeamsFirstRound(conf_name):
    db = db_conexion()
    cursor = db.get_collection('Teams').find(
        {'$and': [{'conf_name': conf_name}, {'stage.firstRound': True}]}).sort(
        'fifa_nation_rank', 1)
    listData = list(cursor)
    return listData


def getTeamsSecondRound(conf_name):
    db = db_conexion()
    cursor = db.get_collection('Teams').find(
        {'$and': [{'conf_name': conf_name}, {'stage.secondRound': True}]}).sort(
        'fifa_nation_rank', 1)
    listData = list(cursor)
    return listData


def getTeamsThirdRound(conf_name):
    db = db_conexion()
    cursor = db.get_collection('Teams').find(
        {'$and': [{'conf_name': conf_name}, {'stage.thirdRound': True}]}).sort(
        'fifa_nation_rank', 1)
    listData = list(cursor)
    return listData


def getTeamsFinalRound(conf_name):
    db = db_conexion()
    cursor = db.get_collection('Teams').find(
        {'$and': [{'conf_name': conf_name}, {'stage.finalRound': True}]}).sort(
        'fifa_nation_rank', 1)
    listData = list(cursor)
    return listData


def getTeamsPlayoff():
    db = db_conexion()
    cursor = db.get_collection('Teams').find({'stage.playoff': True}).sort(
        'fifa_nation_rank', 1)
    listData = list(cursor)
    return listData


def getTeamsMainDraw():
    db = db_conexion()
    cursor = db.get_collection('Teams').find({'stage.mainDraw': True}).sort(
        'fifa_nation_rank', 1)
    listData = list(cursor)
    return listData


def getTeamsCopaAmerica():
    db = db_conexion()
    cursor = db.get_collection('Teams').find({'$or': [{'conf_name': 'CONMEBOL'}, {
        '$and': [{'conf_name': 'CONCACAF'}, {'$or': [{'stage.mainDraw': True}, {'stage.playoff': True}]}]}]}).sort(
        'fifa_nation_rank', 1)
    listData = list(cursor)
    return listData


def updateStage(id, stage):
    db = db_conexion()
    stageObj = {
        'firstRound': True if stage == 'firstRound' else False,
        'secondRound': True if stage == 'secondRound' else False,
        'thirdRound': True if stage == 'thirdRound' else False,
        'finalRound': True if stage == 'finalRound' else False,
        'playoff': True if stage == 'playoff' else False,
        'mainDraw': True if stage == 'mainDraw' else False,
    }
    db.get_collection('Teams').update_one({'id': id}, {'$set': {'stage': stageObj}})


def getTeamsJSON():
    db = db_conexion()
    cursor = db.get_collection('Teams').find({}, {"_id": 0}).sort(
        'fifa_nation_rank', 1)
    listData = list(cursor)
    return listData


def getQualyPlaces(conf):
    db = db_conexion()
    cursor = db.get_collection('Places').find({"conf": conf})
    listData = list(cursor)
    return listData


def getRoundPlaces(placesList, round):
    list = None
    listPlaces = placesList[0]
    match round:
        case 'first':
            list = listPlaces['places']['firstRound']
        case 'second':
            list = listPlaces['places']['secondRound']
        case 'third':
            list = listPlaces['places']['thirdRound']
        case 'final':
            list = listPlaces['places']['finalRound']
    return list


def getTeamById(team):
    db = db_conexion()
    return list(db.get_collection('Teams').find({'id': team}))


def saveMatchResult(fixture, match, localGoals, awayGoals, conf, round, zone):
    db = db_conexion()
    match fixture:
        case 1:
            if match == 1:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture1.match1.homeTeam.goals': localGoals,
                                                              'fixtures.fixture1.match1.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture1.match1.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture1.match1.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture1.match1.played': True}})
            else:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture1.match2.homeTeam.goals': localGoals,
                                                              'fixtures.fixture1.match2.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture1.match2.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture1.match2.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture1.match2.played': True}})
        case 2:
            if match == 1:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture2.match1.homeTeam.goals': localGoals,
                                                              'fixtures.fixture2.match1.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture2.match1.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture2.match1.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture2.match1.played': True}})
            else:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture2.match2.homeTeam.goals': localGoals,
                                                              'fixtures.fixture2.match2.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture2.match2.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture2.match2.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture2.match2.played': True}})
        case 3:
            if match == 1:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture3.match1.homeTeam.goals': localGoals,
                                                              'fixtures.fixture3.match1.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture3.match1.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture3.match1.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture3.match1.played': True}})
            else:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture3.match2.homeTeam.goals': localGoals,
                                                              'fixtures.fixture3.match2.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture3.match2.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture3.match2.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture3.match2.played': True}})
        case 4:
            if match == 1:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture4.match1.homeTeam.goals': localGoals,
                                                              'fixtures.fixture4.match1.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture4.match1.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture4.match1.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture4.match1.played': True}})
            else:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture4.match2.homeTeam.goals': localGoals,
                                                              'fixtures.fixture4.match2.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture4.match2.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture4.match2.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture4.match2.played': True}})
        case 5:
            if match == 1:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture5.match1.homeTeam.goals': localGoals,
                                                              'fixtures.fixture5.match1.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture5.match1.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture5.match1.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture5.match1.played': True}})
            else:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture5.match2.homeTeam.goals': localGoals,
                                                              'fixtures.fixture5.match2.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture5.match2.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture5.match2.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture5.match2.played': True}})
        case 6:
            if match == 1:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture6.match1.homeTeam.goals': localGoals,
                                                              'fixtures.fixture6.match1.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture6.match1.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture6.match1.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture6.match1.played': True}})
            else:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture6.match2.homeTeam.goals': localGoals,
                                                              'fixtures.fixture6.match2.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture6.match2.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture6.match2.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture6.match2.played': True}})
        case 7:
            if match == 1:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture7.match1.homeTeam.goals': localGoals,
                                                              'fixtures.fixture7.match1.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture7.match1.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture7.match1.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture7.match1.played': True}})
            else:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture7.match2.homeTeam.goals': localGoals,
                                                              'fixtures.fixture7.match2.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture7.match2.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture7.match2.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture7.match2.played': True}})
        case 8:
            if match == 1:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture8.match1.homeTeam.goals': localGoals,
                                                              'fixtures.fixture8.match1.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture8.match1.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture8.match1.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture8.match1.played': True}})
            else:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture8.match2.homeTeam.goals': localGoals,
                                                              'fixtures.fixture8.match2.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture8.match2.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture8.match2.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture8.match2.played': True}})
        case 9:
            if match == 1:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture9.match1.homeTeam.goals': localGoals,
                                                              'fixtures.fixture9.match1.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture9.match1.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture9.match1.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture9.match1.played': True}})
            else:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture9.match2.homeTeam.goals': localGoals,
                                                              'fixtures.fixture9.match2.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture9.match2.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture9.match2.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture9.match2.played': True}})
        case _:
            if match == 1:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture10.match1.homeTeam.goals': localGoals,
                                                              'fixtures.fixture10.match1.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture10.match1.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture10.match1.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture10.match1.played': True}})
            else:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture10.match2.homeTeam.goals': localGoals,
                                                              'fixtures.fixture10.match2.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture10.match2.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture10.match2.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture10.match2.played': True}})


def saveExtraTimeResult(fixture, match, localGoals, awayGoals, localPenaltys, awayPenaltys, conf, round, zone,
                        homeTeam=None, awayTeam=None):
    db = db_conexion()
    match fixture:
        case 'first':
            if match == 1:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.first.match1.homeTeam.goals': localGoals,
                                                              'fixtures.first.match1.awayTeam.goals': awayGoals,
                                                              'fixtures.first.match1.homeTeam.penalties': localPenaltys if localPenaltys is not None else None,
                                                              'fixtures.first.match1.awayTeam.penalties': awayPenaltys if awayPenaltys is not None else None,
                                                              'fixtures.first.match1.homeTeam.result': True if localGoals > awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys > awayPenaltys) else False,
                                                              'fixtures.first.match1.awayTeam.result': True if localGoals < awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys < awayPenaltys) else False,
                                                              'fixtures.first.match1.played': True}})
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.final.match1.awayTeam.team': homeTeam if localGoals > awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys > awayPenaltys) else awayTeam}})

            if match == 2:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.first.match2.homeTeam.goals': localGoals,
                                                              'fixtures.first.match2.awayTeam.goals': awayGoals,
                                                              'fixtures.first.match2.homeTeam.penalties': localPenaltys if localPenaltys is not None else None,
                                                              'fixtures.first.match2.awayTeam.penalties': awayPenaltys if awayPenaltys is not None else None,
                                                              'fixtures.first.match2.homeTeam.result': True if localGoals > awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys > awayPenaltys) else False,
                                                              'fixtures.first.match2.awayTeam.result': True if localGoals < awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys < awayPenaltys) else False,
                                                              'fixtures.first.match2.played': True}})
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.final.match2.awayTeam.team': homeTeam if localGoals > awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys > awayPenaltys) else awayTeam}})
            if match == 3:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.first.match3.homeTeam.goals': localGoals,
                                                              'fixtures.first.match3.awayTeam.goals': awayGoals,
                                                              'fixtures.first.match3.homeTeam.penalties': localPenaltys if localPenaltys is not None else None,
                                                              'fixtures.first.match3.awayTeam.penalties': awayPenaltys if awayPenaltys is not None else None,
                                                              'fixtures.first.match3.homeTeam.result': True if localGoals > awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys > awayPenaltys) else False,
                                                              'fixtures.first.match3.awayTeam.result': True if localGoals < awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys < awayPenaltys) else False,
                                                              'fixtures.first.match3.played': True}})
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.final.match3.awayTeam.team': homeTeam if localGoals > awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys > awayPenaltys) else awayTeam}})
            if match == 4:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.first.match4.homeTeam.goals': localGoals,
                                                              'fixtures.first.match4.awayTeam.goals': awayGoals,
                                                              'fixtures.first.match4.homeTeam.penalties': localPenaltys if localPenaltys is not None else None,
                                                              'fixtures.first.match4.awayTeam.penalties': awayPenaltys if awayPenaltys is not None else None,
                                                              'fixtures.first.match4.homeTeam.result': True if localGoals > awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys > awayPenaltys) else False,
                                                              'fixtures.first.match4.awayTeam.result': True if localGoals < awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys < awayPenaltys) else False,
                                                              'fixtures.first.match4.played': True}})
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.final.match4.awayTeam.team': homeTeam if localGoals > awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys > awayPenaltys) else awayTeam}})

        case 'final':
            if match == 1:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.final.match1.homeTeam.goals': localGoals,
                                                              'fixtures.final.match1.awayTeam.goals': awayGoals,
                                                              'fixtures.final.match1.homeTeam.penalties': localPenaltys if localPenaltys is not None else None,
                                                              'fixtures.final.match1.awayTeam.penalties': awayPenaltys if awayPenaltys is not None else None,
                                                              'fixtures.final.match1.homeTeam.result': True if localGoals > awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys > awayPenaltys) else False,
                                                              'fixtures.final.match1.awayTeam.result': True if localGoals < awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys < awayPenaltys) else False,
                                                              'fixtures.final.match1.played': True}})

            if match == 2:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.final.match2.homeTeam.goals': localGoals,
                                                              'fixtures.final.match2.awayTeam.goals': awayGoals,
                                                              'fixtures.final.match2.homeTeam.penalties': localPenaltys if localPenaltys is not None else None,
                                                              'fixtures.final.match2.awayTeam.penalties': awayPenaltys if awayPenaltys is not None else None,
                                                              'fixtures.final.match2.homeTeam.result': True if localGoals > awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys > awayPenaltys) else False,
                                                              'fixtures.final.match2.awayTeam.result': True if localGoals < awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys < awayPenaltys) else False,
                                                              'fixtures.final.match2.played': True}})
            if match == 3:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.final.match3.homeTeam.goals': localGoals,
                                                              'fixtures.final.match3.awayTeam.goals': awayGoals,
                                                              'fixtures.final.match3.homeTeam.penalties': localPenaltys if localPenaltys is not None else None,
                                                              'fixtures.final.match3.awayTeam.penalties': awayPenaltys if awayPenaltys is not None else None,
                                                              'fixtures.final.match3.homeTeam.result': True if localGoals > awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys > awayPenaltys) else False,
                                                              'fixtures.final.match3.awayTeam.result': True if localGoals < awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys < awayPenaltys) else False,
                                                              'fixtures.final.match3.played': True}})
            if match == 4:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.final.match4.homeTeam.goals': localGoals,
                                                              'fixtures.final.match4.awayTeam.goals': awayGoals,
                                                              'fixtures.final.match4.homeTeam.penalties': localPenaltys if localPenaltys is not None else None,
                                                              'fixtures.final.match4.awayTeam.penalties': awayPenaltys if awayPenaltys is not None else None,
                                                              'fixtures.final.match4.homeTeam.result': True if localGoals > awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys > awayPenaltys) else False,
                                                              'fixtures.final.match4.awayTeam.result': True if localGoals < awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys < awayPenaltys) else False,
                                                              'fixtures.final.match4.played': True}})
            if match == 5:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.final.match5.homeTeam.goals': localGoals,
                                                              'fixtures.final.match5.awayTeam.goals': awayGoals,
                                                              'fixtures.final.match5.homeTeam.penalties': localPenaltys if localPenaltys is not None else None,
                                                              'fixtures.final.match5.awayTeam.penalties': awayPenaltys if awayPenaltys is not None else None,
                                                              'fixtures.final.match5.homeTeam.result': True if localGoals > awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys > awayPenaltys) else False,
                                                              'fixtures.final.match5.awayTeam.result': True if localGoals < awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys < awayPenaltys) else False,
                                                              'fixtures.final.match5.played': True}})

            if match == 6:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.final.match6.homeTeam.goals': localGoals,
                                                              'fixtures.final.match6.awayTeam.goals': awayGoals,
                                                              'fixtures.final.match6.homeTeam.penalties': localPenaltys if localPenaltys is not None else None,
                                                              'fixtures.final.match6.awayTeam.penalties': awayPenaltys if awayPenaltys is not None else None,
                                                              'fixtures.final.match6.homeTeam.result': True if localGoals > awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys > awayPenaltys) else False,
                                                              'fixtures.final.match6.awayTeam.result': True if localGoals < awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys < awayPenaltys) else False,
                                                              'fixtures.final.match6.played': True}})
            if match == 7:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.final.match7.homeTeam.goals': localGoals,
                                                              'fixtures.final.match7.awayTeam.goals': awayGoals,
                                                              'fixtures.final.match7.homeTeam.penalties': localPenaltys if localPenaltys is not None else None,
                                                              'fixtures.final.match7.awayTeam.penalties': awayPenaltys if awayPenaltys is not None else None,
                                                              'fixtures.final.match7.homeTeam.result': True if localGoals > awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys > awayPenaltys) else False,
                                                              'fixtures.final.match7.awayTeam.result': True if localGoals < awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys < awayPenaltys) else False,
                                                              'fixtures.final.match7.played': True}})
            if match == 8:
                db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.final.match8.homeTeam.goals': localGoals,
                                                              'fixtures.final.match8.awayTeam.goals': awayGoals,
                                                              'fixtures.final.match8.homeTeam.penalties': localPenaltys if localPenaltys is not None else None,
                                                              'fixtures.final.match8.awayTeam.penalties': awayPenaltys if awayPenaltys is not None else None,
                                                              'fixtures.final.match8.homeTeam.result': True if localGoals > awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys > awayPenaltys) else False,
                                                              'fixtures.final.match8.awayTeam.result': True if localGoals < awayGoals or (
                                                                      localGoals == awayGoals and localPenaltys < awayPenaltys) else False,
                                                              'fixtures.final.match8.played': True}})
        case _:
            db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                      {'$set': {
                                                          'fixtures.wildCard.match1.homeTeam.goals': localGoals,
                                                          'fixtures.wildCard.match1.awayTeam.goals': awayGoals,
                                                          'fixtures.wildCard.match1.homeTeam.penalties': localPenaltys if localPenaltys is not None else None,
                                                          'fixtures.wildCard.match1.awayTeam.penalties': awayPenaltys if awayPenaltys is not None else None,
                                                          'fixtures.first.match1.homeTeam.result': True if localGoals > awayGoals or (
                                                                  localGoals == awayGoals and localPenaltys > awayPenaltys) else False,
                                                          'fixtures.wildCard.match1.awayTeam.result': True if localGoals < awayGoals or (
                                                                  localGoals == awayGoals and localPenaltys < awayPenaltys) else False,
                                                          'fixtures.wildCard.match1.played': True}})


def diferencia_media(local, visita):
    return True if (abs(local - visita) > 10) and (abs(local - visita) < 21) else False


def diferencia_alta(local, visita):
    return True if (abs(local - visita) > 20) and (abs(local - visita) < 31) else False


def diferencia_extrema(local, visita):
    return True if ((abs(local - visita) > 30) and (abs(local - visita) < 71)) else False

def diferencia_ultra(local, visita):
    return True if (abs(local - visita) > 70) else False
