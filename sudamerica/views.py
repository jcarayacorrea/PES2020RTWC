from django.shortcuts import render


# Create your views here.
def finalround(request):
    return render(request, 'sudamerica/finalround.html')