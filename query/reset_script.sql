#CONMEBOL
db.Teams.find({conf_name:"CONMEBOL"}).sort({fifa_nation_rank: 1}).map((team)=>{
    let stage = {
        firstRound: false,
        secondRound: false,
        thirdRound: false,
        finalRound: true
    }
    db.Teams.updateOne({id: team.id},{$set:{stage:stage}})
});

#UEFA
db.Teams.find({conf_name:"UEFA"}).sort({fifa_nation_rank: 1}).limit(12).map((team)=>{
    let stage = {
        firstRound: false,
        secondRound: false,
        thirdRound: false,
        finalRound: true
    }
    db.Teams.updateOne({id: team.id},{$set:{stage:stage}})
});
db.Teams.find({conf_name:"UEFA"}).sort({fifa_nation_rank: 1}).skip(12).limit(12).map((team)=>{
    let stage = {
        firstRound: false,
        secondRound: false,
        thirdRound: true,
        finalRound: false
    }
    db.Teams.updateOne({id: team.id},{$set:{stage:stage}})
});
db.Teams.find({conf_name:"UEFA"}).sort({fifa_nation_rank: 1}).skip(24).limit(21).map((team)=>{
    let stage = {
        firstRound: false,
        secondRound: true,
        thirdRound: false,
        finalRound: false
    }
    db.Teams.updateOne({id: team.id},{$set:{stage:stage}})
});
db.Teams.find({conf_name:"UEFA"}).sort({fifa_nation_rank: -1}).limit(10).map((team)=>{
    let stage = {
        firstRound: true,
        secondRound: false,
        thirdRound: false,
        finalRound: false
    }
    db.Teams.updateOne({id: team.id},{$set:{stage:stage}})
});

#CAF
db.Teams.find({conf_name:"CAF"}).sort({fifa_nation_rank: 1}).limit(15).map((team)=>{
    let stage = {
        firstRound: false,
        secondRound: false,
        thirdRound: false,
        finalRound: true
    }
    db.Teams.updateOne({id: team.id},{$set:{stage:stage}})
});
db.Teams.find({conf_name:"CAF"}).sort({fifa_nation_rank: 1}).skip(15).limit(10).map((team)=>{
    let stage = {
        firstRound: false,
        secondRound: false,
        thirdRound: true,
        finalRound: false
    }
    db.Teams.updateOne({id: team.id},{$set:{stage:stage}})
});
db.Teams.find({conf_name:"CAF"}).sort({fifa_nation_rank: 1}).skip(25).limit(17).map((team)=>{
    let stage = {
        firstRound: false,
        secondRound: true,
        thirdRound: false,
        finalRound: false
    }
    db.Teams.updateOne({id: team.id},{$set:{stage:stage}})
});
db.Teams.find({conf_name:"CAF"}).sort({fifa_nation_rank: -1}).limit(12).map((team)=>{
    let stage = {
        firstRound: true,
        secondRound: false,
        thirdRound: false,
        finalRound: false
    }
    db.Teams.updateOne({id: team.id},{$set:{stage:stage}})
});

#AFC
db.Teams.find({conf_name:"AFC"}).sort({fifa_nation_rank: 1}).limit(8).map((team)=>{
    let stage = {
        firstRound: false,
        secondRound: false,
        thirdRound: false,
        finalRound: true
    }
    db.Teams.updateOne({id: team.id},{$set:{stage:stage}})
});
db.Teams.find({conf_name:"AFC"}).sort({fifa_nation_rank: 1}).skip(8).limit(12).map((team)=>{
    let stage = {
        firstRound: false,
        secondRound: false,
        thirdRound: true,
        finalRound: false
    }
    db.Teams.updateOne({id: team.id},{$set:{stage:stage}})
});
db.Teams.find({conf_name:"AFC"}).sort({fifa_nation_rank: 1}).skip(20).limit(22).map((team)=>{
    let stage = {
        firstRound: false,
        secondRound: true,
        thirdRound: false,
        finalRound: false
    }
    db.Teams.updateOne({id: team.id},{$set:{stage:stage}})
});
db.Teams.find({conf_name:"AFC"}).sort({fifa_nation_rank: -1}).limit(4).map((team)=>{
    let stage = {
        firstRound: true,
        secondRound: false,
        thirdRound: false,
        finalRound: false
    }
    db.Teams.updateOne({id: team.id},{$set:{stage:stage}})
});

#CONCACAF
db.Teams.find({conf_name:"CONCACAF"}).sort({fifa_nation_rank: 1}).limit(10).map((team)=>{
    let stage = {
        firstRound: false,
        secondRound: false,
        thirdRound: false,
        finalRound: true
    }
    db.Teams.updateOne({id: team.id},{$set:{stage:stage}})
});
db.Teams.find({conf_name:"CONCACAF"}).sort({fifa_nation_rank: 1}).skip(10).map((team)=>{
    let stage = {
        firstRound: true,
        secondRound: false,
        thirdRound: false,
        finalRound: false
    }
    db.Teams.updateOne({id: team.id},{$set:{stage:stage}})
});
#OFC
db.Teams.find({conf_name:"OFC"}).sort({fifa_nation_rank: 1}).limit(6).map((team)=>{
    let stage = {
        firstRound: false,
        secondRound: false,
        thirdRound: false,
        finalRound: true
    }
    db.Teams.updateOne({id: team.id},{$set:{stage:stage}})
});
db.Teams.find({conf_name:"OFC"}).sort({fifa_nation_rank: -1}).limit(5).map((team)=>{
    let stage = {
        firstRound: true,
        secondRound: false,
        thirdRound: false,
        finalRound: false
    }
    db.Teams.updateOne({id: team.id},{$set:{stage:stage}})
});

db.Fixtures.updateMany({},{$set:{teams:{},fixtures:{}}})