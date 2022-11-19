from django.shortcuts import render

# Create your views here.
def finalround(request):
    return render(request,'oceania/finalround.html')

def firstround(request):
    return render(request,'oceania/fstround.html')