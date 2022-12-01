from pymongo import MongoClient


def db_conexion():
    client = MongoClient(host='localhost',
                         port=27017,
                         username='admin',
                         password='mongo')
    db = client['pesrtwc']
    return db


def getTeams(stage, conf_name):

    db = db_conexion()

    if conf_name != None and stage != None:
        teams = db.get_collection('Teams').find({'conf_name': conf_name, 'stage.' + stage: True}).sort(
            'fifa_nation_rank', 1)
    if conf_name != None:
        teams = db.get_collection('Teams').find({'conf_name': conf_name}).sort('fifa_nation_rank', 1)

    if stage == "mainDraw" or stage == "playoff":
        teams = db.get_collection('Teams').find({'stage.' + stage: True}).sort('fifa_nation_rank', 1)
    return teams

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
