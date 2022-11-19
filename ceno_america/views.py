from django.shortcuts import render

# Create your views here.
def finalround(request):
    return render(request,'ncamerica/finalround.html')

def firstround(request):
    return render(request,'ncamerica/fstround.html')