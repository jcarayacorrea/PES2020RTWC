from fixtures import getZoneData


def getStandings(conf, round, zone):
    context = {}
    groupStandings = []
    fixture = getZoneData(zone, conf, round)
    teams = fixture['teams']
    fixtureList = fixtureArray(fixture['fixtures'])
    print(createStandings(fixtureList,teams))


def createStandings(list, teams):
    teamsList = []
    for team in teams:
        teamObj = {}
        teamId = team['id']
        teamObj['team'] = team
        teamObj['points'] = countPoints(teamId, list)
        teamsList.append(teamObj)
    return teamsList


def countPoints(teamId, list):
    points = 0
    for item in list:
        if item is not None:
            if item['match1']['played'] == True:
                if item['match1']['homeTeam']['team']['id'] == teamId:
                    if item['match1']['homeTeam']['result'] == True and item['match1']['awayTeam']['result'] == False:
                        points += 3
                    elif item['match1']['homeTeam']['result'] == False and item['match1']['awayTeam'][
                        'result'] == False:
                        points += 1
                if item['match1']['awayTeam']['team']['id'] == teamId:
                    if item['match1']['awayTeam']['result'] == True and item['match1']['homeTeam']['result'] == False:
                        points += 3
                    elif item['match1']['awayTeam']['result'] == False and item['match1']['homeTeam'][
                        'result'] == False:
                        points += 1
            if item['match2']['played'] == True:
                if item['match2']['homeTeam']['team']['id'] == teamId:
                    if item['match2']['homeTeam']['result'] == True and item['match2']['awayTeam']['result'] == False:
                        points += 3
                    elif item['match2']['homeTeam']['result'] == False and item['match2']['awayTeam'][
                        'result'] == False:
                        points += 1
                if item['match2']['awayTeam']['team']['id'] == teamId:
                    if item['match1']['awayTeam']['result'] == True and item['match2']['homeTeam']['result'] == False:
                        points += 3
                    elif item['match2']['awayTeam']['result'] == False and item['match2']['homeTeam'][
                        'result'] == False:
                        points += 1
    return points


def localGolDiff(teamId, list):
    return


def awayGolDiff(teamId, list):
    return


def fixtureArray(fixtures):
    fixtureList = []
    fixtureList.append(fixtures.get('fixture1'))
    fixtureList.append(fixtures.get('fixture2'))
    fixtureList.append(fixtures.get('fixture3'))
    fixtureList.append(fixtures.get('fixture4'))
    fixtureList.append(fixtures.get('fixture5'))
    fixtureList.append(fixtures.get('fixture6'))
    fixtureList.append(fixtures.get('fixture7'))
    fixtureList.append(fixtures.get('fixture8'))
    fixtureList.append(fixtures.get('fixture9'))
    fixtureList.append(fixtures.get('fixture10'))

    return fixtureList
