from django.urls import path
from . import views

urlpatterns = [
    path('teamlist/', views.teams, name='sudamerica.teams'),
    path('teamlist/updateProgress/<str:code>/<str:stage>', views.update_progress, name='sudamerica.updateProgress'),
    path('copaamerica/', views.copa_america, name='sudamerica.copaamerica'),
    path('copaamerica/draw/', views.copa_america_button, name='sudamerica.copaamerica.draw'),
]

