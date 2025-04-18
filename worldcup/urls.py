from django.urls import path
from . import views

urlpatterns = [
    path('maindraw/', views.maindraw, name='worldcup.maindraw'),
    path('maindraw/draw/', views.draw_main_button, name='worldcup.draw'),
    path('playoff/', views.playoff, name='worldcup.playoff'),
    path('playoff/draw', views.getPlayoffPage, name='worldcup.playoff.draw'),

]
