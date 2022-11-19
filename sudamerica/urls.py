from django.urls import path
from . import views

urlpatterns = [
    path('finalround/', views.finalround, name='sudamerica.finalround')
]

