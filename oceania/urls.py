from django.urls import path
from . import views

urlpatterns = [
    path('finalround/', views.finalround, name='oceania.finalround'),
    path('firstround/', views.firstround, name='oceania.firstround')
]