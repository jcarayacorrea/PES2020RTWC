from django.urls import path
from . import views

urlpatterns = [
    path('playoff/', views.euro_playoff, name='europa.playoff'),
    path('playoff/draw', views.get_playoff_page, name='europa.playoff.draw'),
    path('finalround/', views.final_round, name='europa.finalround'),
    path('finalround/draw', views.final_round_button, name='europa.finalround.draw'),
    path('firstround/', views.first_round, name='europa.firstround'),
    path('firstround/draw/', views.first_round_button, name='europa.firstround.draw'),
    path('teamlist/', views.teams, name='europa.teams'),
    path('teamlist/updateProgress/<str:code>/<str:stage>', views.update_progress, name='europa.updateProgress')
]
