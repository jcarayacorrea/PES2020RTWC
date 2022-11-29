from django.shortcuts import render
from utils import db_conexion



# Create your views here.
def finalround(request):
    context = {}
    context['teams'] = getTeams()
    return render(request, 'sudamerica/finalround.html',context)

def getTeams():
    db = db_conexion()
    return db.get_collection('Teams').find({'conf_name':'CONMEBOL'}).sort('fifa_nation_rank',1)