from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from utils import getTeams, updateStage


# Create your views here.
def finalround(request):
    context = {}
    context['teams'] = getTeams(stage=None,conf_name='CONMEBOL')
    return render(request, 'sudamerica/finalround.html', context)


def updateProgress(request,id, stage):
    if request.method == 'POST':
        updateStage(id,stage)
    return   redirect('sudamerica.finalround')
