from django.urls import path
from . import views

urlpatterns = [
    path('finalround/', views.finalround, name='sudamerica.finalround'),
    path('finalround/updateProgress/<str:id>/<str:stage>', views.updateProgress, name= 'sudamerica.updateProgress'),
    path('copaamerica/', views.copaAmerica, name='sudamerica.copaamerica'),
    path('copaamerica/draw/', views.copaAmericaButton, name='sudamerica.copaamerica.draw'),
]

