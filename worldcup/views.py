from django.shortcuts import render

# Create your views here.
def maindraw(request):
    return render(request,'worldcup/maindraw.html')

def playoff(request):
    return render(request,'worldcup/playoff.html')
