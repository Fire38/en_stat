from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, render_to_response
from datetime import datetime


from .models import *
from .sql_requests import *
from .graphics import *

import plotly.graph_objects as go

CURRENT_YEAR_START = datetime.strptime('01/1/2019', '%m/%d/%Y').date()


# Create your views here.
def index(request, year=2019):
    games_count = get_games_count(year)
    authors_count = get_authors_count(year)
    players_count = get_players_count(year)
    teams_count = get_teams_count(year)

    max_resonance_game = get_max_forum_resonance(year)
    max_quality_game = get_best_game_quality(year)

    best_team_list = get_best_team_list(year)
    top3_best_team = best_team_list[:3]

    codes_count = get_code_count(year)

    authors_and_game_count_list = get_all_authors_and_count_game(year)
    top3_authors = authors_and_game_count_list[:3]
    authors_dict = get_author_and_his_games(year)
    often_player_list = get_often_player_list(year)
    often_players = often_player_list[:3]
    often_teams_list = get_often_team(year)
    top3_often_teams = often_teams_list[:3]
    # print(often_team)

    rate_list = get_players_rate_list(year)
    good_rate_players = rate_list[:5]
    strict_rate_players = rate_list[-5:]


    div = author_graph(year)
    forum_resonance_graphic = forum_resonance_bar(year)
    quality_graphic = quality_top_bar(year)
    total_player_per_year_graphic = total_players_per_year_bar()
    total_team_per_year_graphic = total_teams_per_year_bar()

    if year == 2019:
        total_players_per_month_graphic = total_teams_per_month_bar(year)
        total_teams_per_month_graphic = total_players_per_month_bar(year)
        total_teams_per_game_graphic = total_teams_per_game_bar(year)
        total_players_per_game_graphic = total_players_per_game_bar(year)
    else:
        total_players_per_month_graphic = 0
        total_teams_per_month_graphic = 0
        total_teams_per_game_graphic = 0
        total_players_per_game_graphic = 0
    return render(request, 'backend/index.html', {'games_count': games_count,
                                                  'authors_count': authors_count,
                                                  'players_count': players_count,
                                                  'teams_count': teams_count,
                                                  'max_resonance_game': max_resonance_game,
                                                  'max_quality_game': max_quality_game,
                                                  'top3_best_team': top3_best_team,
                                                  'winner_list': best_team_list,
                                                  'codes_count': codes_count,
                                                  'best_authors': top3_authors,
                                                  'authors_dict': authors_dict,
                                                  'often_players': often_players,
                                                  'often_player_list': often_player_list,
                                                  'often_teams_list': often_teams_list,
                                                  'top3_often_team': top3_often_teams,
                                                  'rate_list': rate_list,
                                                  'good_rate_players': good_rate_players,
                                                  'strict_rate_players': strict_rate_players,

                                                  'div': div,
                                                  'forum_resonance_graph': forum_resonance_graphic,
                                                  'quality_graphic': quality_graphic,
                                                  'total_player_graphic': total_player_per_year_graphic,
                                                  'total_players_per_month_graphic': total_players_per_month_graphic,
                                                  'total_team_graphic': total_team_per_year_graphic,
                                                  'total_teams_per_month_graphic': total_teams_per_month_graphic,
                                                  'total_teams_per_game_graphic': total_teams_per_game_graphic,
                                                  'total_players_per_game_graphic': total_players_per_game_graphic,


                                                  'year': year

                                                  })

def sql_requests(request):
    return HttpResponse('<p>ПРивет!</p>')