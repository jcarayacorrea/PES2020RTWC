from django.shortcuts import render, redirect
from utils import getTeams, updateStage


# Create your views here.
def finalround(request):
    return render(request,'africa/finalround.html')

def thirdround(request):
    return render(request,'africa/thrround.html')

def secondround(request):
    return render(request,'africa/sndround.html')

def firstround(request):
    return render(request,'africa/fstround.html')

def teams(request):
    context = {}
    context['teams'] = getTeams(conf_name='CAF',stage=None)
    return render(request,'africa/teamlist.html',context)

def updateProgress(request,id, stage):
    if request.method == 'POST':
        updateStage(id,stage)
    return  redirect('africa.teams')