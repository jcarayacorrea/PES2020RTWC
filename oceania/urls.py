from django.urls import path
from . import views

urlpatterns = [
    path('finalround/', views.final_round, name='oceania.finalround'),
    path('finalround/draw/', views.final_round_button, name='oceania.finalround.draw'),
    path('firstround/', views.first_round, name='oceania.firstround'),
    path('firstround/draw/', views.first_round_button, name='oceania.firstround.draw'),
    path('homemaindraw/', views.set_home_final_team, name='oceania.homemainDraw'),
    path('awaymaindraw/', views.set_away_final_team, name='oceania.awaymainDraw'),
    path('teamlist/', views.teams, name='oceania.teams'),
    path('teamlist/updateProgress/<str:code>/<str:stage>', views.update_progress, name='oceania.updateProgress')
]
