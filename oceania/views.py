from django.shortcuts import render, redirect
from utils import updateStage, getTeams, getTeamsFirstRound, getTeamsFinalRound


# Create your views here.
def finalround(request):
    context = {}
    context['teams'] = getTeamsFinalRound(conf_name='OFC')
    return render(request,'oceania/finalround.html',context)

def firstround(request):
    context = {}
    context['teams'] = getTeamsFirstRound(conf_name='OFC')
    return render(request,'oceania/fstround.html',context)

def teams(request):
    context = {}
    context['teams'] = getTeams(conf_name='OFC')
    return render(request,'oceania/teamlist.html',context)

def updateProgress(request,id, stage):
    if request.method == 'POST':
        updateStage(id,stage)
    return  redirect('oceania.teams')