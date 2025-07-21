from django.urls import path
from . import views

urlpatterns = [
    path('finalround/', views.finalround, name='oceania.finalround'),
    path('finalround/draw/', views.finalRoundButton, name='oceania.finalround.draw'),
    path('firstround/', views.firstround, name='oceania.firstround'),
    path('firstround/draw/', views.firstRoundButton, name='oceania.firstround.draw'),
    path('homemaindraw/', views.setHomeFinalTeam, name='oceania.homemainDraw'),
    path('awaymaindraw/', views.setAwayFinalTeam, name='oceania.awaymainDraw'),
    path('teamlist/', views.teams, name='oceania.teams'),
    path('teamlist/updateProgress/<str:code>/<str:stage>', views.updateProgress, name='oceania.updateProgress')

]
