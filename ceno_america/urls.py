from django.urls import path
from . import views

urlpatterns = [
    path('finalround/', views.finalround, name='ceno_america.finalround'),
    path('firstround/', views.firstround, name='ceno_america.firstround'),
    path('teamlist/', views.teams, name='ceno_america.teams'),
    path('teamlist/updateProgress/<str:id>/<str:stage>', views.updateProgress, name= 'ceno_america.updateProgress')
]
