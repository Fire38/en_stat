from django.shortcuts import render
from datetime import datetime


from .models import *
from .sql_requests import *
from .graphics import *

import plotly.graph_objects as go

CURRENT_YEAR_START = datetime.strptime('01/1/2019', '%m/%d/%Y').date()


# Create your views here.
def index(request, year=2010):
    games_count = get_games_count(year)
    authors_count = get_authors_count(year)
    players_count = get_players_count(year)
    teams_count = get_teams_count(year)
    max_resonance_game = get_max_forum_resonance(year)
    max_quality_game = get_best_game_quality(year)
    best_team = get_best_team(year)
    winner_list = get_top_best_team(year)
    codes_count = get_code_count(year)
    best_author = get_author(year)
    author_and_game_count_list = get_all_authors_and_game(year)
    authors_dict = get_author_and_his_games(year)
    often_player = get_often_player(year)
    often_player_list = get_often_player_list(year)
    often_team = get_often_team(year)
    # print(often_team)

    div = author_graph(year)
    forum_resonance_graphic = forum_resonance_graph(year)
    quality_graphic = quality_top_graph(year)
    return render(request, 'backend/index.html', {'games_count': games_count,
                                                  'authors_count': authors_count,
                                                  'players_count': players_count,
                                                  'teams_count': teams_count,
                                                  'max_resonance_game': max_resonance_game,
                                                  'max_quality_game': max_quality_game,
                                                  'best_team': best_team,
                                                  'winner_list': winner_list,
                                                  'codes_count': codes_count,
                                                  'best_author': best_author,
                                                  'authors_dict': authors_dict,
                                                  'often_player': often_player,
                                                  'often_player_list': often_player_list,
                                                  'often_team': often_team,

                                                  'div': div,
                                                  'forum_resonance_graph': forum_resonance_graphic,
                                                  'quality_graphic': quality_graphic

                                                  })