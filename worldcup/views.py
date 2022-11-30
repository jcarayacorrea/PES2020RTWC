from django.shortcuts import render

from utils import db_conexion


# Create your views here.
def maindraw(request):
    context = {}
    context['teams'] = getTeams('mainDraw')
    return render(request,'worldcup/maindraw.html',context)

def playoff(request):
    context = {}
    context['teams'] = getTeams('playoff')
    return render(request,'worldcup/playoff.html',context)

def getTeams(stage):
    db = db_conexion()
    return db.get_collection('Teams').find({'stage.mainDraw': True}).sort('fifa_nation_rank', 1) if stage == 'mainDraw' else db.get_collection('Teams').find({'stage.playoff': True}).sort('fifa_nation_rank', 1)
