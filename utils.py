from bson.json_util import dumps
from pymongo import MongoClient


def db_conexion():
    client = MongoClient(host='localhost',
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
                db.get_collection('Fixtures').update_many({'conf_name': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture1.match1.homeTeam.goals': localGoals,
                                                              'fixtures.fixture1.match1.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture1.match1.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture1.match1.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture1.match1.played': True}})
            else:
                db.get_collection('Fixtures').update_many({'conf_name': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture1.match2.homeTeam.goals': localGoals,
                                                              'fixtures.fixture1.match2.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture1.match2.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture1.match2.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture1.match2.played': True}})
        case 2:
            if match == 1:
                db.get_collection('Fixtures').update_many({'conf_name': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture2.match1.homeTeam.goals': localGoals,
                                                              'fixtures.fixture2.match1.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture2.match1.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture2.match1.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture2.match1.played': True}})
            else:
                db.get_collection('Fixtures').update_many({'conf_name': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture2.match2.homeTeam.goals': localGoals,
                                                              'fixtures.fixture2.match2.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture2.match2.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture2.match2.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture2.match2.played': True}})
        case 3:
            if match == 1:
                db.get_collection('Fixtures').update_many({'conf_name': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture3.match1.homeTeam.goals': localGoals,
                                                              'fixtures.fixture3.match1.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture3.match1.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture3.match1.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture3.match1.played': True}})
            else:
                db.get_collection('Fixtures').update_many({'conf_name': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture3.match2.homeTeam.goals': localGoals,
                                                              'fixtures.fixture3.match2.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture3.match2.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture3.match2.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture3.match2.played': True}})
        case 4:
            if match == 1:
                db.get_collection('Fixtures').update_many({'conf_name': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture4.match1.homeTeam.goals': localGoals,
                                                              'fixtures.fixture4.match1.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture4.match1.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture4.match1.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture4.match1.played': True}})
            else:
                db.get_collection('Fixtures').update_many({'conf_name': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture4.match2.homeTeam.goals': localGoals,
                                                              'fixtures.fixture4.match2.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture4.match2.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture4.match2.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture4.match2.played': True}})
        case 5:
            if match == 1:
                db.get_collection('Fixtures').update_many({'conf_name': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture5.match1.homeTeam.goals': localGoals,
                                                              'fixtures.fixture5.match1.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture5.match1.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture5.match1.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture5.match1.played': True}})
            else:
                db.get_collection('Fixtures').update_many({'conf_name': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture5.match2.homeTeam.goals': localGoals,
                                                              'fixtures.fixture5.match2.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture5.match2.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture5.match2.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture5.match2.played': True}})
        case 6:
            if match == 1:
                db.get_collection('Fixtures').update_many({'conf_name': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture6.match1.homeTeam.goals': localGoals,
                                                              'fixtures.fixture6.match1.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture6.match1.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture6.match1.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture6.match1.played': True}})
            else:
                db.get_collection('Fixtures').update_many({'conf_name': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture6.match2.homeTeam.goals': localGoals,
                                                              'fixtures.fixture6.match2.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture6.match2.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture6.match2.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture6.match2.played': True}})
        case 7:
            if match == 1:
                db.get_collection('Fixtures').update_many({'conf_name': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture7.match1.homeTeam.goals': localGoals,
                                                              'fixtures.fixture7.match1.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture7.match1.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture7.match1.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture7.match1.played': True}})
            else:
                db.get_collection('Fixtures').update_many({'conf_name': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture7.match2.homeTeam.goals': localGoals,
                                                              'fixtures.fixture7.match2.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture7.match2.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture7.match2.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture7.match2.played': True}})
        case 8:
            if match == 1:
                db.get_collection('Fixtures').update_many({'conf_name': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture8.match1.homeTeam.goals': localGoals,
                                                              'fixtures.fixture8.match1.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture8.match1.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture8.match1.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture8.match1.played': True}})
            else:
                db.get_collection('Fixtures').update_many({'conf_name': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture8.match2.homeTeam.goals': localGoals,
                                                              'fixtures.fixture8.match2.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture8.match2.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture8.match2.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture8.match2.played': True}})
        case 9:
            if match == 1:
                db.get_collection('Fixtures').update_many({'conf_name': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture9.match1.homeTeam.goals': localGoals,
                                                              'fixtures.fixture9.match1.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture9.match1.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture9.match1.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture9.match1.played': True}})
            else:
                db.get_collection('Fixtures').update_many({'conf_name': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture9.match2.homeTeam.goals': localGoals,
                                                              'fixtures.fixture9.match2.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture9.match2.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture9.match2.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture9.match2.played': True}})
        case _:
            if match == 1:
                db.get_collection('Fixtures').update_many({'conf_name': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture10.match1.homeTeam.goals': localGoals,
                                                              'fixtures.fixture10.match1.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture10.match1.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture10.match1.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture10.match1.played': True}})
            else:
                db.get_collection('Fixtures').update_many({'conf_name': conf, 'round': round, 'zone': zone},
                                                          {'$set': {
                                                              'fixtures.fixture10.match2.homeTeam.goals': localGoals,
                                                              'fixtures.fixture10.match2.awayTeam.goals': awayGoals,
                                                              'fixtures.fixture10.match2.homeTeam.result': True if localGoals > awayGoals else False,
                                                              'fixtures.fixture10.match2.awayTeam.result': True if localGoals < awayGoals else False,
                                                              'fixtures.fixture10.match2.played': True}})
