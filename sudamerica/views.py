from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from utils import db_conexion


# Create your views here.
def finalround(request):
    context = {}
    context['teams'] = getTeams()
    return render(request, 'sudamerica/finalround.html', context)


def getTeams():
    db = db_conexion()
    return db.get_collection('Teams').find({'conf_name': 'CONMEBOL'}).sort('fifa_nation_rank', 1)


def updateProgress(request,id, stage):
    if request.method == 'POST':

        db = db_conexion()
        stageObj = {
            'firstRound': True if stage == 'firstRound'  else False,
            'secondRound': True if stage == 'secondRound' else False,
            'thirdRound': True if stage == 'thirdRound' else False,
            'finalRound': True if stage == 'finalRound' else False,
            'playoff': True if stage == 'playoff' else False,
            'mainDraw': True if stage == 'mainDraw' else False,
        }
        print(stageObj)

        db.get_collection('Teams').update_one({'id': id}, {'$set': {'stage': stageObj}})
    return redirect('sudamerica.finalround')
