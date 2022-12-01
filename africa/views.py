from django.shortcuts import render, redirect
from utils import getTeams, updateStage, getTeamsFirstRound, getTeamsSecondRound, getTeamsThirdRound, getTeamsFinalRound


# Create your views here.
def finalround(request):
    context = {}
    context['teams'] = getTeamsFinalRound(conf_name='CAF')
    return render(request,'africa/finalround.html',context)

def thirdround(request):
    context = {}
    context['teams'] = getTeamsThirdRound(conf_name='CAF')
    return render(request,'africa/thrround.html',context)

def secondround(request):
    context = {}
    context['teams'] = getTeamsSecondRound(conf_name='CAF')
    return render(request,'africa/sndround.html',context)

def firstround(request):
    context = {}
    context['teams'] = getTeamsFirstRound(conf_name='CAF')
    return render(request,'africa/fstround.html',context)

def teams(request):
    context = {}
    context['teams'] = getTeams(conf_name='CAF')
    return render(request,'africa/teamlist.html',context)

def updateProgress(request,id, stage):
    if request.method == 'POST':
        updateStage(id,stage)
    return  redirect('africa.teams')