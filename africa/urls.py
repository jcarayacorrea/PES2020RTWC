from django.urls import path
from . import views

urlpatterns = [
    path('finalround/', views.finalround, name='africa.finalround'),
    path('secondround/', views.secondround, name='africa.secondround'),
    path('firstround/', views.firstround, name='africa.firstround')
]
