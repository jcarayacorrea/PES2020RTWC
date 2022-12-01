from django.shortcuts import render, redirect
from utils import db_conexion, getTeams, updateStage, getTeamsFirstRound, getTeamsSecondRound, getTeamsThirdRound, \
    getTeamsFinalRound


# Create your views here.
def finalround(request):
    context = {}
    context['teams'] = getTeamsFinalRound(conf_name='AFC')
    return render(request,'asia/finalround.html',context)

def thirdround(request):
    context = {}
    context['teams'] = getTeamsThirdRound(conf_name='AFC')
    return render(request,'asia/thrround.html',context)

def secondround(request):
    context = {}
    context['teams'] = getTeamsSecondRound(conf_name='AFC')
    return render(request,'asia/sndround.html',context)

def firstround(request):
    context = {}
    context['teams'] = getTeamsFirstRound(conf_name='AFC')
    return render(request,'asia/fstround.html',context)

def teams(request):
    context = {}
    context['teams'] = getTeams(conf_name='AFC')
    return render(request,'asia/teamlist.html',context)

def updateProgress(request,id, stage):
    if request.method == 'POST':
        updateStage(id,stage)
    return  redirect('asia.teams')