from django.urls import path
from . import views

urlpatterns = [
    path('finalround/', views.final_round, name='africa.finalround'),
    path('finalround/draw', views.final_round_button, name='africa.finalround.draw'),
    path('thirdround/', views.third_round, name='africa.thirdround'),
    path('thirdround/draw', views.third_round_button, name='africa.thirdround.draw'),
    path('secondround/', views.second_round, name='africa.secondround'),
    path('secondround/draw', views.second_round_button, name='africa.secondround.draw'),
    path('firstround/', views.first_round, name='africa.firstround'),
    path('firstround/draw/', views.first_round_button, name='africa.firstround.draw'),
    path('teamlist/', views.teams, name='africa.teams'),
    path('teamlist/updateProgress/<str:code>/<str:stage>', views.update_progress, name='africa.updateProgress')
]
