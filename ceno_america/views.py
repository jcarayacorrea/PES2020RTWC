from django.shortcuts import render, redirect
from utils import db_conexion, updateStage, getTeams


# Create your views here.
def finalround(request):
    return render(request,'ncamerica/finalround.html')

def firstround(request):
    return render(request,'ncamerica/fstround.html')


def teams(request):
    context = {}
    context['teams'] = getTeams(conf_name='CONCACAF',stage=None)
    return render(request,'ncamerica/teamlist.html',context)

def updateProgress(request,id, stage):
    if request.method == 'POST':
        updateStage(id,stage)
    return  redirect('ncamerica.teams')