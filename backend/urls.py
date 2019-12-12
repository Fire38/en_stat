from django.urls import path
from .views import *

urlpatterns = [
    path('index', index, name='index'),
    path('index/<int:year>/', index, name='index_year'),
    path('get_rating_information', get_rating_information, name='rating_information'),
    path('get_team_information', get_team_information, name='team_information'),
    path('get_main_count_information', get_main_count_information, name='main_count_information'),
    path('get_main_top_information', get_main_top_information, name='main_top_information'),
    path('get_main_players_information', get_main_players_information, name='main_players_information'),

    path('get_total_per_year_graphics', get_total_players_per_year_graphic, name='total_players_graphic'),
    path('get_total_per_month_graphics', get_total_players_per_month_graphic, name='total_players_per_month_graphic'),
    path('get_total_per_game_graphics', get_total_players_per_game_graphic, name='total_players_per_game_graphic'),
    path('get_quality_and_forum_resonance_graphics', get_quality_and_forum_resonance_graphic, name='quality_and_forum_resonance_graphics'),
    path('get_often_players_graphics', get_often_players_graphic, name='often_players_graphics'),
    path('get_often_and_winner_teams_graphics', get_often_and_winner_teams_graphic, name='often_and_winner_teams_graphic')
]