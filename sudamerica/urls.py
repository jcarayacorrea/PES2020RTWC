from django.urls import path
from . import views

urlpatterns = [
    path('teamlist/', views.teams, name='sudamerica.teams'),
    path('teamlist/updateProgress/<str:code>/<str:stage>', views.updateProgress, name= 'sudamerica.updateProgress'),
    path('copaamerica/', views.copaAmerica, name='sudamerica.copaamerica'),
    path('copaamerica/draw/', views.copaAmericaButton, name='sudamerica.copaamerica.draw'),
]

