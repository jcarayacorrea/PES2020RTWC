from django.shortcuts import render, redirect
from utils import db_conexion, updateStage, getTeams


# Create your views here.
def finalround(request):
    return render(request,'oceania/finalround.html')

def firstround(request):
    return render(request,'oceania/fstround.html')

def teams(request):
    context = {}
    context['teams'] = getTeams(conf_name='OFC',stage=None)
    return render(request,'oceania/teamlist.html',context)

def updateProgress(request,id, stage):
    if request.method == 'POST':
        updateStage(id,stage)
    return  redirect('oceania.teams')