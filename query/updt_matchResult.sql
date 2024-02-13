db.Fixtures.updateMany({'conf':'FIFA','round':'playoff', 'zone': 'P'},{$set:{
'fixtures.final.match2.homeTeam.goals': 2,
'fixtures.final.match2.awayTeam.goals': 1,
'fixtures.final.match2.awayTeam.result': false,
'fixtures.final.match2.homeTeam.result': true,
'fixtures.final.match2.played': true,
}})

