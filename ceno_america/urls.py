from django.urls import path
from . import views

urlpatterns = [
    path('finalround/', views.finalround, name='ceno_america.finalround'),
    path('firstround/', views.firstround, name='ceno_america.firstround')
]
