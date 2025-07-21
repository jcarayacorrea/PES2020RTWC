from django.urls import path
from . import views

urlpatterns = [
    path('finalround/', views.finalround, name='asia.finalround'),
    path('finalround/draw', views.finalRoundButton, name='asia.finalround.draw'),
    path('thirdround/', views.thirdround, name='asia.thirdround'),
    path('thirdround/draw', views.thirdRoundButton, name='asia.thirdround.draw'),
    path('secondround/', views.secondround, name='asia.secondround'),
    path('secondround/draw', views.secondRoundButton, name='asia.secondround.draw'),
    path('firstround/', views.firstround, name='asia.firstround'),
    path('firstround/draw/', views.firstRoundButton, name='asia.firstround.draw'),
    path('teamlist/', views.teams, name='asia.teams'),
    path('teamlist/updateProgress/<str:code>/<str:stage>', views.updateProgress, name= 'asia.updateProgress')
]
