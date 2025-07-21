from django.urls import path
from . import views

urlpatterns = [
    path('finalround/', views.finalround, name='cenoamerica.finalround'),
    path('finalround/draw/', views.finalRoundButton, name='cenoamerica.finalround.draw'),
    path('firstround/', views.firstround, name='cenoamerica.firstround'),
    path('firstround/draw/', views.firstRoundButton, name='cenoamerica.firstround.draw'),
    path('teamlist/', views.teams, name='cenoamerica.teams'),
    path('teamlist/updateProgress/<str:code>/<str:stage>', views.updateProgress, name='cenoamerica.updateProgress')
]
