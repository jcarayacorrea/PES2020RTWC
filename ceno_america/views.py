from django.shortcuts import render, redirect
from utils import updateStage, getTeams, getTeamsFinalRound, getTeamsFirstRound


# Create your views here.
def finalround(request):
    context = {}
    context['teams'] = getTeamsFinalRound(conf_name='CONCACAF')
    return render(request,'ncamerica/finalround.html',context)

def firstround(request):
    context = {}
    context['teams'] = getTeamsFirstRound(conf_name='CONCACAF')
    return render(request,'ncamerica/fstround.html',context)


def teams(request):
    context = {}
    context['teams'] = getTeams(conf_name='CONCACAF')
    return render(request,'ncamerica/teamlist.html',context)

def updateProgress(request,id, stage):
    if request.method == 'POST':
        updateStage(id,stage)
    return  redirect('ncamerica.teams')