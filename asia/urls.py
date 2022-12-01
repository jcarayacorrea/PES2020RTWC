from django.urls import path
from . import views

urlpatterns = [
    path('finalround/', views.finalround, name='asia.finalround'),
    path('thirdround/', views.thirdround, name='asia.thirdround'),
    path('secondround/', views.secondround, name='asia.secondround'),
    path('firstround/', views.firstround, name='asia.firstround'),
    path('teamlist/', views.teams, name='asia.teams'),
    path('teamlist/updateProgress/<str:id>/<str:stage>', views.updateProgress, name= 'asia.updateProgress')
]
