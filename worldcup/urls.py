from django.urls import path
from . import views

urlpatterns = [
    path('maindraw/', views.main_draw, name='worldcup.maindraw'),
    path('maindraw/draw/', views.draw_main_button, name='worldcup.draw'),
    path('playoff/', views.playoff, name='worldcup.playoff'),
    path('playoff/draw', views.get_playoff_page, name='worldcup.playoff.draw'),
]
