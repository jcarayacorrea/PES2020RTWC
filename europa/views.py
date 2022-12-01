from django.shortcuts import render, redirect
from utils import db_conexion, getTeams, updateStage


# Create your views here.
def finalround(request):
    return render(request,'europa/finalround.html')

def thirdround(request):
    return render(request, 'europa/thrround.html')

def secondround(request):
    return render(request, 'europa/sndround.html')

def firstround(request):
    return render(request,'europa/fstround.html')

def teams(request):
    context = {}
    context['teams'] = getTeams(conf_name='UEFA',stage=None)
    return render(request,'europa/teamlist.html',context)

def updateProgress(request,id, stage):
    if request.method == 'POST':
        updateStage(id,stage)
    return  redirect('europa.teams')