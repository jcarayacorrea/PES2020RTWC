from django.urls import path
from . import views

urlpatterns = [
    path('maindraw/', views.maindraw, name='worldcup.maindraw'),
    path('maindraw/draw/', views.maindrawButton, name='worldcup.draw'),
    path('playoff/', views.playoff, name='worldcup.playoff'),

]
