from django.urls import path
from . import views

urlpatterns = [
    path('finalround/', views.final_round, name='cenoamerica.finalround'),
    path('finalround/draw/', views.final_round_button, name='cenoamerica.finalround.draw'),
    path('firstround/', views.first_round, name='cenoamerica.firstround'),
    path('firstround/draw/', views.first_round_button, name='cenoamerica.firstround.draw'),
    path('teamlist/', views.teams, name='cenoamerica.teams'),
    path('teamlist/updateProgress/<str:code>/<str:stage>', views.update_progress, name='cenoamerica.updateProgress')
]
