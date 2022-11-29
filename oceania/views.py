from django.shortcuts import render
from utils import db_conexion

# Create your views here.
def finalround(request):
    return render(request,'oceania/finalround.html')

def firstround(request):
    return render(request,'oceania/fstround.html')

def teams(request):
    context = {}
    context['teams'] = getTeams()
    return render(request,'oceania/teamlist.html',context)

def getTeams():
    db = db_conexion()
    return db.get_collection('Teams').find({'conf_name':'OFC'}).sort('fifa_nation_rank',1)