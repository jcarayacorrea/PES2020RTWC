from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('flag-showcase/', views.flag_showcase, name='flag.showcase'),
    path('api/teams/', views.get_team_list, name='api.teams'),
    path('fixtures/<str:conf>/<str:round_name>/<str:zone>', views.fixture_zone, name='zones.fixtures'),
    path('standings/<str:conf>/<str:round_name>/<str:zone>', views.standings_zone, name='zones.standings'),
    path('sim/', views.sim_match, name='match_simulator'),
    path('api/download_draw/', views.download_draw, name='api.download')
]
