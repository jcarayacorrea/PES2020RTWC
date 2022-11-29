from django.shortcuts import render
from utils import db_conexion

# Create your views here.
def finalround(request):
    return render(request,'ncamerica/finalround.html')

def firstround(request):
    return render(request,'ncamerica/fstround.html')

def teams(request):
    context= {}
    context['teams'] = getTeams()
    return render(request,'ncamerica/teamlist.html',context)

def getTeams():
    db = db_conexion()
    return db.get_collection('Teams').find({'conf_name':'CONCACAF'}).sort('fifa_nation_rank',1)