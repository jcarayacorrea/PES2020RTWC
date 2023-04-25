from fixtures import getZoneData
from operator import itemgetter


def getStandings(conf, round, zone):
    context = {}
    groupStandings = []
    fixture = getZoneData(zone, conf, round)
    teams = fixture['teams']
    fixtureList = fixtureArray(fixture['fixtures'])
    return createStandings(fixtureList, teams)


def createStandings(list, teams):
    teamsList = []
    for team in teams:
        teamObj = {}
        teamId = team['id']
        teamObj['team'] = team
        points, matches = countPoints(teamId, list)
        golFavor, golContra, golLocal, golVisita, diff = goaldifference(teamId, list)
        teamObj['points'] = points
        teamObj['matches'] = matches
        teamObj['favor'] = golFavor
        teamObj['against'] = golContra
        teamObj['local'] = golLocal
        teamObj['away'] = golVisita
        teamObj['difference'] = diff
        teamsList.append(teamObj)

    return sorted(teamsList, key=itemgetter('points', 'difference', 'favor', 'away'), reverse=True)


def countPoints(teamId, list):
    points = 0
    matches = 0
    for item in list:
        if item is not None:
            if item.get('match1') is not None:
                if item['match1']['played'] == True:
                    matches += 1
                    if item['match1']['homeTeam']['team']['id'] == teamId:
                        if item['match1']['homeTeam']['result'] == True and item['match1']['awayTeam'][
                            'result'] == False:
                            points += 3
                        elif item['match1']['homeTeam']['result'] == False and item['match1']['awayTeam'][
                            'result'] == False:
                            points += 1
                    if item['match1']['awayTeam']['team']['id'] == teamId:
                        if item['match1']['awayTeam']['result'] == True and item['match1']['homeTeam'][
                            'result'] == False:
                            points += 3
                        elif item['match1']['awayTeam']['result'] == False and item['match1']['homeTeam'][
                            'result'] == False:
                            points += 1

            if item.get('match2') is not None:
                if item['match2']['played'] == True:
                    matches += 1
                    if item['match2']['homeTeam']['team']['id'] == teamId:
                        if item['match2']['homeTeam']['result'] == True and item['match2']['awayTeam'][
                            'result'] == False:
                            points += 3
                        elif item['match2']['homeTeam']['result'] == False and item['match2']['awayTeam'][
                            'result'] == False:
                            points += 1
                    if item['match2']['awayTeam']['team']['id'] == teamId:
                        if item['match2']['awayTeam']['result'] == True and item['match2']['homeTeam'][
                            'result'] == False:
                            points += 3
                        elif item['match2']['awayTeam']['result'] == False and item['match2']['homeTeam'][
                            'result'] == False:
                            points += 1
    return points, matches


def goaldifference(teamId, list):
    localGoalsF = 0
    awayGoalsF = 0
    localGoalsC = 0
    awayGoalsC = 0
    for item in list:
        if item is not None:
            if item.get('match1') is not None:
                if item['match1']['played'] == True:

                    if item['match1']['homeTeam']['team']['id'] == teamId:
                        localGoalsF += item['match1']['homeTeam']['goals']
                        localGoalsC += item['match1']['awayTeam']['goals']
                    if item['match1']['awayTeam']['team']['id'] == teamId:
                        awayGoalsF += item['match1']['awayTeam']['goals']
                        awayGoalsC += item['match1']['homeTeam']['goals']

            if item.get('match2') is not None:
                if item['match2']['played'] == True:
                    if item['match2']['homeTeam']['team']['id'] == teamId:
                        localGoalsF += item['match2']['homeTeam']['goals']
                        localGoalsC += item['match2']['awayTeam']['goals']
                    if item['match2']['awayTeam']['team']['id'] == teamId:
                        awayGoalsF += item['match1']['awayTeam']['goals']
                        awayGoalsC += item['match1']['homeTeam']['goals']
    teamGoalsF = localGoalsF + awayGoalsF
    teamGoalsC = localGoalsC + awayGoalsC
    return teamGoalsF, teamGoalsC, localGoalsF, awayGoalsF, (teamGoalsF - teamGoalsC)


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
