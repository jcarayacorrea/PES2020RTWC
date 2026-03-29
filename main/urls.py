from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/teams/', views.get_team_list, name='api.teams'),
    path('fixtures/<str:conf>/<str:round_name>/<str:zone>', views.fixture_zone, name='zones.fixtures'),
    path('standings/<str:conf>/<str:round_name>/<str:zone>', views.standings_zone, name='zones.standings'),
    path('match_simulator/<int:fixture>/<int:match>/<str:home_id>/<str:away_id>/<str:conf>/<str:round_name>/<str:zone>/<int:extra_time>/<int:single_load>',
         views.sim_match,
         name='match_simulator'),
    path(
        'extra_time/<str:fixture>/<int:match>/<str:home_id>/<str:away_id>/<str:conf>/<str:round_name>/<str:zone>/<int:extra_time>',
        views.sim_match,
        name='one_match'),
    path('api/download_draw/', views.download_draw, name='api.download')
]
