from django.urls import path
from . import views

urlpatterns = [
    path('playoff/', views.euroPlayoff, name='europa.playoff'),
    path('playoff/draw', views.getPlayoffPage, name='europa.playoff.draw'),
    path('finalround/', views.finalround, name='europa.finalround'),
    path('finalround/draw', views.finalRoundButton, name='europa.finalround.draw'),
    path('firstround/', views.firstround, name='europa.firstround'),
    path('firstround/draw/', views.firstRoundButton, name='europa.firstround.draw'),
    path('teamlist/', views.teams, name='europa.teams'),
    path('teamlist/updateProgress/<str:code>/<str:stage>', views.updateProgress, name='europa.updateProgress')
]
