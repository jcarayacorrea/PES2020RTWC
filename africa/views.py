from django.shortcuts import render
from utils import db_conexion

# Create your views here.
def finalround(request):
    return render(request,'africa/finalround.html')

def thirdround(request):
    return render(request,'africa/thrround.html')

def secondround(request):
    return render(request,'africa/sndround.html')

def firstround(request):
    return render(request,'africa/fstround.html')

def teams(request):
    context = {}
    context['teams'] = getTeams()
    return render(request,'africa/teamlist.html',context)

def getTeams():
    db = db_conexion()
    return db.get_collection('Teams').find({'conf_name':'CAF'}).sort('fifa_nation_rank',1)