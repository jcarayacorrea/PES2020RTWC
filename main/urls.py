from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/teams/', views.teamListApi, name='api.teams'),
    path('fixtures/<str:conf>/<str:round>/<str:zone>', views.fixtureZone, name='zones.fixtures'),
    path('standings/<str:conf>/<str:round>/<str:zone>', views.standingsZone, name='zones.standings'),
    path('match_simulator/<int:fixture>/<int:match>/<str:homeId>/<str:awayId>/<str:conf>/<str:round>/<str:zone>',
         views.sim_match,
         name='match_simulator')
]
