from django.urls import path
from . import views

urlpatterns = [
    path('finalround/', views.finalround, name='europa.finalround'),
    path('thirdround/', views.thirdround, name='europa.thirdround'),
    path('secondround/', views.secondround, name='europa.secondround'),
    path('firstround/', views.firstround, name='europa.firstround'),
    path('teamlist/', views.teams, name='europa.teams'),
    path('teamlist/updateProgress/<str:id>/<str:stage>', views.updateProgress, name= 'europa.updateProgress')
]
