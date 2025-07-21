from django.urls import path
from . import views

urlpatterns = [
    path('finalround/', views.finalround, name='africa.finalround'),
    path('finalround/draw', views.finalRoundButton, name='africa.finalround.draw'),
    path('thirdround/', views.thirdround, name='africa.thirdround'),
    path('thirdround/draw', views.thirdRoundButton, name='africa.thirdround.draw'),
    path('secondround/', views.secondround, name='africa.secondround'),
    path('secondround/draw', views.secondRoundButton, name='africa.secondround.draw'),
    path('firstround/', views.firstround, name='africa.firstround'),
    path('firstround/draw/', views.firstRoundButton, name='africa.firstround.draw'),
    path('teamlist/', views.teams, name='africa.teams'),
    path('teamlist/updateProgress/<str:code>/<str:stage>', views.updateProgress, name='africa.updateProgress')
]
