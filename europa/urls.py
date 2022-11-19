from django.urls import path
from . import views

urlpatterns = [
    path('finalround/', views.finalround, name='europa.finalround'),
    path('secondround/', views.secondround, name='europa.secondround'),
    path('firstround/', views.firstround, name='europa.firstround')
]
