from django.shortcuts import render

# Create your views here.
def finalround(request):
    return render(request,'europa/finalround.html')

def secondround(request):
    return render(request,'europa/sndround.html')

def firstround(request):
    return render(request,'europa/fstround.html')