from django.urls import path
from . import views

urlpatterns = [
    path('finalround/', views.finalround, name='europa.finalround'),
    path('finalround/draw', views.finalRoundButton, name='europa.finalround.draw'),
    path('thirdround/', views.thirdround, name='europa.thirdround'),
    path('thirdround/draw', views.thirdRoundButton, name='europa.thirdround.draw'),
    path('secondround/', views.secondround, name='europa.secondround'),
    path('secondround/draw', views.secondRoundButton, name='europa.secondround.draw'),
    path('firstround/', views.firstround, name='europa.firstround'),
    path('firstround/draw/', views.firstRoundButton, name='europa.firstround.draw'),
    path('teamlist/', views.teams, name='europa.teams'),
    path('teamlist/updateProgress/<str:id>/<str:stage>', views.updateProgress, name='europa.updateProgress')
]
