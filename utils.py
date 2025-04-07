from pymongo import MongoClient


GROUP_RANGE = ['1','2','3','4','5']
GROUP_CODES = ['A','B','C','D','E','F','G','H']
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


def get_filter_conditions():
    conf_name_or_condition = {"$or": [{"conf_name": "CONMEBOL"}, {"conf_name": "CONCACAF"}]}
    stage_or_condition = {"$or": [{"stage.mainDraw": True}, {"stage.playoff": True}]}
    combined_and_condition = {"$and": [conf_name_or_condition, stage_or_condition]}
    return {"$or": [conf_name_or_condition, combined_and_condition]}


def getTeamsCopaAmerica():
    db = db_conexion()
    filter_conditions = get_filter_conditions()
    cursor = db.get_collection('Teams').find(filter_conditions).sort('fifa_nation_rank', 1)
    listData = list(cursor)
    return listData


def generateStageObj(stage):
    stages = ['firstRound', 'secondRound', 'thirdRound', 'finalRound', 'playoff', 'mainDraw']
    return {stage_key: stage_key == stage for stage_key in stages}


def updateStage(id, stage):
    db = db_conexion()
    stageObj = generateStageObj(stage)
    idObj = {'id': id}
    db.get_collection('Teams').update_one(idObj, {'$set': {'stage': stageObj}})


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


def get_stage_data(stage, places):
    stage_data = {
        'first': places['places']['firstRound'],
        'second': places['places']['secondRound'],
        'third': places['places']['thirdRound'],
        'final': places['places']['finalRound']
    }
    return stage_data.get(stage)


def get_round_stages(places_list, stage):
    places = places_list[0]
    stage_list = get_stage_data(stage, places)
    return stage_list


def getTeamById(team):
    db = db_conexion()
    return list(db.get_collection('Teams').find({'id': team}))


def saveMatchResult(fixture, match, localGoals, awayGoals, conf, round, zone):
    db = db_conexion()

    def update_match_results(fixture_num, match_num, local_goals, away_goals):
        match_path = f'fixtures.fixture{fixture_num}.match{match_num}'

        db.get_collection('Fixtures').update_many({'conf': conf, 'round': round, 'zone': zone},
                                                  {'$set': {
                                                      f'{match_path}.homeTeam.goals': local_goals,
                                                      f'{match_path}.awayTeam.goals': away_goals,
                                                      f'{match_path}.homeTeam.result': local_goals > away_goals,
                                                      f'{match_path}.awayTeam.result': local_goals < away_goals,
                                                      f'{match_path}.played': True}})

    update_match_results(fixture, match, localGoals, awayGoals)


def create_match_spec(phase, match_num, localGoals, awayGoals, localPenaltys, awayPenaltys):
    return {
        f'fixtures.{phase}.match{match_num}.homeTeam.goals': localGoals,
        f'fixtures.{phase}.match{match_num}.awayTeam.goals': awayGoals,
        f'fixtures.{phase}.match{match_num}.homeTeam.penalties': localPenaltys,
        f'fixtures.{phase}.match{match_num}.awayTeam.penalties': awayPenaltys,
        f'fixtures.{phase}.match{match_num}.homeTeam.result': localGoals > awayGoals or (
                localGoals == awayGoals and localPenaltys > awayPenaltys),
        f'fixtures.{phase}.match{match_num}.awayTeam.result': localGoals < awayGoals or (
                localGoals == awayGoals and localPenaltys < awayPenaltys),
        f'fixtures.{phase}.match{match_num}.played': True
    }


def saveExtraTimeResult(phase, match, localGoals, awayGoals, localPenaltys, awayPenaltys, conf, round, zone):
    db = db_conexion()
    final_match_spec = create_match_spec(phase, match, localGoals, awayGoals, localPenaltys, awayPenaltys)
    db.get_collection('Fixtures').update_many(
        {'conf': conf, 'round': round, 'zone': zone}, {'$set': final_match_spec})



def is_difference_in_range(local_score, visitor_score, range_start, range_end):
    difference = abs(local_score - visitor_score)
    return range_start < difference < range_end


def medium_difference(local_score, visitor_score):
    return is_difference_in_range(local_score, visitor_score, 10, 21)


def high_difference(local_score, visitor_score):
    return is_difference_in_range(local_score, visitor_score, 20, 31)


def extreme_difference(local_score, visitor_score):
    return is_difference_in_range(local_score, visitor_score, 30, 71)


def ultra_difference(local_score, visitor_score):
    return is_difference_in_range(local_score, visitor_score, 70, float('inf'))

