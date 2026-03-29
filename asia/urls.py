from django.urls import path
from . import views

urlpatterns = [
    path('finalround/', views.final_round, name='asia.finalround'),
    path('finalround/draw', views.final_round_button, name='asia.finalround.draw'),
    path('thirdround/', views.third_round, name='asia.thirdround'),
    path('thirdround/draw', views.third_round_button, name='asia.thirdround.draw'),
    path('secondround/', views.second_round, name='asia.secondround'),
    path('secondround/draw', views.second_round_button, name='asia.secondround.draw'),
    path('firstround/', views.first_round, name='asia.firstround'),
    path('firstround/draw/', views.first_round_button, name='asia.firstround.draw'),
    path('teamlist/', views.teams, name='asia.teams'),
    path('teamlist/updateProgress/<str:code>/<str:stage>', views.update_progress, name='asia.updateProgress')
]
