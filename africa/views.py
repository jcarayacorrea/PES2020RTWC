from django.shortcuts import render

# Create your views here.
def finalround(request):
    return render(request,'africa/finalround.html')

def thirdround(request):
    return render(request,'africa/thrround.html')

def secondround(request):
    return render(request,'africa/sndround.html')

def firstround(request):
    return render(request,'africa/fstround.html')