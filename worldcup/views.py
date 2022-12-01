from django.shortcuts import render

from utils import getTeams


# Create your views here.
def maindraw(request):
    context = {}
    context['teams'] = getTeams('mainDraw', conf_name=None)
    return render(request,'worldcup/maindraw.html',context)

def playoff(request):
    context = {}
    context['teams'] = getTeams('playoff', conf_name=None)
    return render(request,'worldcup/playoff.html',context)

