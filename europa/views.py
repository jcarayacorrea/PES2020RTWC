from django.shortcuts import render, redirect
from utils import  getTeams, updateStage, getTeamsFinalRound, getTeamsThirdRound, getTeamsSecondRound, \
    getTeamsFirstRound


# Create your views here.

def finalround(request):
    context = {}
    context['teams'] = getTeamsFinalRound(conf_name='UEFA')
    return render(request,'europa/finalround.html',context)

def thirdround(request):
    context = {}
    context['teams'] = getTeamsThirdRound(conf_name='UEFA')
    return render(request,'europa/thrround.html',context)

def secondround(request):
    context = {}
    context['teams'] = getTeamsSecondRound(conf_name='UEFA')
    return render(request,'europa/sndround.html',context)

def firstround(request):
    context = {}
    context['teams'] = getTeamsFirstRound(conf_name='UEFA')
    return render(request,'europa/fstround.html',context)

def teams(request):
    context = {}
    context['teams'] = getTeams(conf_name='UEFA')
    return render(request,'europa/teamlist.html',context)

def updateProgress(request,id, stage):
    if request.method == 'POST':
        updateStage(id,stage)
    return  redirect('europa.teams')