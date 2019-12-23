from django.conf import settings

from django.urls import include, path
from .views import *

urlpatterns = [
    path('index', index, name='index'),
    path('index/<int:year>/', index, name='index_year'),
    #path('get_rating_information', get_rating_information, name='rating_information'),
    #path('get_team_information', get_team_information, name='team_information'),
    path('get_main_count_information', get_main_count_information, name='main_count_information'),
    path('get_main_top_information', get_main_top_information, name='main_top_information'),
    path('get_main_players_information', get_main_players_information, name='main_players_information'),

    path('get_often_players_graphics', get_often_players_graphic, name='often_players_graphics'),
    path('get_often_and_winner_teams_graphics', get_often_and_winner_teams_graphic, name='often_and_winner_teams_graphic')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns