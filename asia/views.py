from django.shortcuts import render

# Create your views here.
def finalround(request):
    return render(request,'asia/finalround.html')

def thirdround(request):
    return render(request,'asia/thrround.html')

def secondround(request):
    return render(request,'asia/sndround.html')

def firstround(request):
    return render(request,'asia/fstround.html')