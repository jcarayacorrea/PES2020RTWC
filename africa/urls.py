from django.urls import path
from . import views

urlpatterns = [
    path('finalround/', views.finalround, name='africa.finalround'),
    path('secondround/', views.secondround, name='africa.secondround'),
    path('thirdround/', views.thirdround, name='africa.thirdround'),
    path('firstround/', views.firstround, name='africa.firstround'),
    path('teamlist/', views.teams, name='africa.teams')
]
