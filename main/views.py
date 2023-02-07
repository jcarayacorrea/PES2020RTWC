from django.http import JsonResponse
from django.shortcuts import render
from django.template.defaulttags import register

from utils import getTeamsJSON
from fixtures import getZoneData


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def teamListApi(request):
    if request.method == 'GET':
        data = getTeamsJSON()
        return JsonResponse(data,safe=False)

def fixtureZone(request,conf,round,zone):
    context = {}
    fixtureDict = getZoneData(zone, conf, round)
    context['fixture'] = fixtureDict['fixtures']
    return render(request,'popups/fixtures/fixture.html',context)

def standingsZone(request,conf,round,zone):
    context = {}
    fixtureDict = getZoneData(zone, conf, round)
    lenght = len(fixtureDict['teams']) + 1
    context['teams'] = zip(fixtureDict['teams'],range(1,lenght))

    return render(request,'popups/standings/standings.html',context)

@register.filter
def getItem(dict,key):
    return dict.get(key)
