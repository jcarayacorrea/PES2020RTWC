from django.urls import path
from . import views

urlpatterns = [
    path('finalround/', views.finalround, name='oceania.finalround'),
    path('finalround/draw/', views.finalRoundButton, name='oceania.finalround.draw'),
    path('firstround/', views.firstround, name='oceania.firstround'),
    path('firstround/draw/', views.firstRoundButton, name='oceania.firstround.draw'),
    path('teamlist/', views.teams, name='oceania.teams'),
    path('teamlist/updateProgress/<str:id>/<str:stage>', views.updateProgress, name='oceania.updateProgress')

]
