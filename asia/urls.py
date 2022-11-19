from django.urls import path
from . import views

urlpatterns = [
    path('finalround/', views.finalround, name='asia.finalround'),
    path('secondround/', views.secondround, name='asia.secondround'),
    path('firstround/', views.firstround, name='asia.firstround')
]
