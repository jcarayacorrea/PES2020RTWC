from django.http import JsonResponse
from django.shortcuts import render

from utils import getTeamsJSON


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def teamListApi(request):
    if request.method == 'GET':
        data = getTeamsJSON()
        return JsonResponse(data,safe=False)
