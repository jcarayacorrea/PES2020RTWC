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
    return db.get_collection('Teams').find({'conf_name': conf_name}).sort('fifa_nation_rank', 1)



def getTeamsFirstRound(conf_name):
    db = db_conexion()
    return  db.get_collection('Teams').find(
                    {'$and': [{'conf_name': conf_name}, {'stage.firstRound': True}]}).sort(
                'fifa_nation_rank', 1)

def getTeamsSecondRound(conf_name):
    db = db_conexion()
    return  db.get_collection('Teams').find(
                    {'$and': [{'conf_name': conf_name}, {'stage.secondRound': True}]}).sort(
                    'fifa_nation_rank', 1)
def getTeamsThirdRound(conf_name):
    db = db_conexion()
    return  db.get_collection('Teams').find(
                    {'$and': [{'conf_name': conf_name}, {'stage.thirdRound': True}]}).sort(
                    'fifa_nation_rank', 1)

def getTeamsFinalRound(conf_name):
    db = db_conexion()
    return db.get_collection('Teams').find(
                    {'$and': [{'conf_name': conf_name}, {'stage.finalRound': True}]}).sort(
                    'fifa_nation_rank', 1)


def getTeamsPlayoff():
    db = db_conexion()
    return db.get_collection('Teams').find({'stage.playoff': True}).sort(
        'fifa_nation_rank', 1)


def getTeamsMainDraw():
    db = db_conexion()
    return db.get_collection('Teams').find({'stage.mainDraw': True}).sort(
            'fifa_nation_rank', 1)

def updateStage(id,stage):
    db = db_conexion()
    stageObj = {
        'firstRound': True if stage == 'firstRound' else False,
        'secondRound': True if stage == 'secondRound' else False,
        'thirdRound': True if stage == 'thirdRound' else False,
        'finalRound': True if stage == 'finalRound' else False,
        'playoff': True if stage == 'playoff' else False,
        'mainDraw': True if stage == 'mainDraw' else False,
    }
    print(stageObj)

    db.get_collection('Teams').update_one({'id': id}, {'$set': {'stage': stageObj}})
