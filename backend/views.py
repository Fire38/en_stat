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
    #games_count = get_games_count(year)
    #authors_count = get_authors_count(year)
    #players_count = get_players_count(year)
    #teams_count = get_teams_count(year)

    #max_resonance_game = get_max_forum_resonance(year)
    #max_quality_game = get_best_game_quality(year)

    #best_team_list = get_best_team_list(year)
    #top3_best_team = best_team_list[:3]

    #codes_count = get_code_count(year)

    #authors_and_game_count_list = get_all_authors_and_count_game(year)
    #top3_authors = authors_and_game_count_list[:3]
    authors_dict = get_author_and_his_games(year)
    #often_player_list = get_often_player_list(year)
    #often_players = often_player_list[:3]
    #often_teams_list = get_often_team(year)
    #top3_often_teams = often_teams_list[:3]
    # print(often_team)

    #rate_list = get_players_rate_list(year)
    #good_rate_players = rate_list[:5]
    #strict_rate_players = rate_list[-5:]


    div = author_graph(year)
    #forum_resonance_graphic = forum_resonance_bar(year)
    #quality_graphic = quality_top_bar(year)
    #total_player_per_year_graphic = total_players_per_year_bar()
    #total_team_per_year_graphic = total_teams_per_year_bar()

    """
    if year == 2019:
        #total_players_per_month_graphic = total_teams_per_month_bar(year)
        #total_teams_per_month_graphic = total_players_per_month_scatter(year)
        #total_teams_per_game_graphic = total_teams_per_game_bar(year)
        #total_players_per_game_graphic = total_players_per_game_bar(year)
    else:
        total_players_per_month_graphic = 0
        total_teams_per_month_graphic = 0
        total_teams_per_game_graphic = 0
        total_players_per_game_graphic = 0"""
    return render(request, 'backend/index.html', {#'games_count': games_count,
                                                  #'authors_count': authors_count,
                                                  #'players_count': players_count,
                                                  #'teams_count': teams_count,
                                                  #'max_resonance_game': max_resonance_game,
                                                  #'max_quality_game': max_quality_game,
                                                  #'top3_best_team': top3_best_team,
                                                  #'winner_list': best_team_list,
                                                  #'codes_count': codes_count,
                                                  #'best_authors': top3_authors,
                                                  'authors_dict': authors_dict,
                                                  #'often_players': often_players,
                                                  #'often_player_list': often_player_list,
                                                  #'often_teams_list': often_teams_list,
                                                  #'top3_often_team': top3_often_teams,
                                                  #'rate_list': rate_list,
                                                  #'good_rate_players': good_rate_players,
                                                  #'strict_rate_players': strict_rate_players,

                                                  'div': div,
                                                  #'forum_resonance_graph': forum_resonance_graphic,
                                                  #'quality_graphic': quality_graphic,
                                                  #'total_player_graphic': total_player_per_year_graphic,
                                                  #'total_players_per_month_graphic': total_players_per_month_graphic,
                                                  #'total_team_graphic': total_team_per_year_graphic,
                                                  #'total_teams_per_month_graphic': total_teams_per_month_graphic,
                                                  #'total_teams_per_game_graphic': total_teams_per_game_graphic,
                                                  #'total_players_per_game_graphic': total_players_per_game_graphic,


                                                  'year': year

                                                  })


def get_main_count_information(request, year=2019):
    year = int(request.GET.get('year'))
    games_count = get_games_count(year)
    authors_count = get_authors_count(year)
    players_count = get_players_count(year)
    teams_count = get_teams_count(year)
    codes_count = get_code_count(year)
    return render_to_response('backend/main_count_information_template.html', context={'games_count': games_count,
                                                                                       'authors_count': authors_count,
                                                                                       'players_count': players_count,
                                                                                       'teams_count': teams_count,
                                                                                       'codes_count': codes_count
                                                                                       })


def get_main_top_information(request, year=2019):
    year = int(request.GET.get('year'))
    max_resonance_game = get_max_forum_resonance(year)
    max_quality_game = get_best_game_quality(year)

    best_team_list = get_best_team_list(year)
    top3_best_team = best_team_list[:3]

    often_teams_list = get_often_team(year)
    top3_often_teams = often_teams_list[:3]

    authors_and_game_count_list = get_all_authors_and_count_game(year)
    top3_authors = authors_and_game_count_list[:3]

    return render_to_response('backend/main_top_information_template.html', context={'max_resonance_game': max_resonance_game,
                                                                                     'max_quality_game': max_quality_game,
                                                                                     'top3_best_team': top3_best_team,
                                                                                     'top3_often_team': top3_often_teams,
                                                                                     'best_authors': top3_authors
                                                                                     })


def get_main_players_information(request, year=2019):
    year = int(request.GET.get('year'))
    often_player_list = get_often_player_list(year)
    often_players = often_player_list[:3]

    rate_list = get_players_rate_list(year)
    good_rate_players = rate_list[:5]
    strict_rate_players = rate_list[-5:]
    return render_to_response('backend/main_players_information_template.html', context={'good_rate_players': good_rate_players,
                                                                                        'strict_rate_players': strict_rate_players,
                                                                                        'often_players': often_players
                                                                                        })

def get_rating_information(request, year=2019):
    year = int(request.GET.get('year'))
    rate_list = get_players_rate_list(year)
    return render_to_response('backend/rate_list_template.html', context={'rate_list': rate_list})


def get_team_information(request, year=2019):
    year = int(request.GET.get('year'))
    often_teams_list = get_often_team(year)
    best_team_list = get_best_team_list(year)

    return render_to_response('backend/team_template.html', context={'often_teams_list': often_teams_list,
                                                                     'winner_list': best_team_list
                                                                     })


def get_total_players_per_year_graphic(request, year=2019):
    total_player_per_year_graphic = total_players_per_year_bar()
    total_team_per_year_graphic = total_teams_per_year_bar()
    return render_to_response('backend/total_per_year_graphs_template.html', context={'total_player_graphic': total_player_per_year_graphic,
                                                                                       'total_team_graphic': total_team_per_year_graphic
                                                                                       })


def get_total_players_per_month_graphic(request, year=2019):
    year = int(request.GET.get('year'))
    total_players_per_month_graphic = total_teams_per_month_bar(year)
    total_teams_per_month_graphic = total_players_per_month_scatter(year)
    return render_to_response('backend/total_per_month_graphs_template.html', context={'total_players_per_month_graphic': total_players_per_month_graphic,
                                                                                       'total_teams_per_month_graphic': total_teams_per_month_graphic
                                                                                       })


def get_total_players_per_game_graphic(request, year=2019):
    year = int(request.GET.get('year'))
    total_teams_per_game_graphic = total_teams_per_game_bar(year)
    total_players_per_game_graphic = total_players_per_game_bar(year)
    return render_to_response('backend/total_per_game_graphs_template.html', context={'total_teams_per_game_graphic': total_teams_per_game_graphic,
                                                                                      'total_players_per_game_graphic': total_players_per_game_graphic
                                                                                      })


def get_quality_and_forum_resonance_graphic(request, year=2019):
    year = int(request.GET.get('year'))
    forum_resonance_graphic = forum_resonance_bar(year)
    quality_graphic = quality_top_bar(year)
    return render_to_response('backend/quality_and_forum_resonance_template.html', context={'forum_resonance_graph': forum_resonance_graphic,
                                                                                            'quality_graphic': quality_graphic,
                                                                                        })


def get_often_players_graphic(request, year=2019):
    # топ 30 самых частоиграющих + полная таблица
    year = int(request.GET.get('year'))
    often_players_table = get_often_player_list(year)
    often_players_graphic = often_player_bar(year)
    return render_to_response('backend/often_player_template.html', context={'often_player_graph': often_players_graphic,
                                                                             'often_players_table': often_players_table
                                                                             })


def get_often_and_winner_teams_graphic(request, year=2019):
    """графики (топ 20) побед и частотоигрющих команд"""
    year = int(request.GET.get('year'))
    often_team_graphic = often_team_bar(year)
    winner_team_graphic = winner_team_bar(year)
    best_team_list = get_best_team_list(year)
    often_team_list = get_often_team(year)
    return render_to_response('backend/often_and_winner_teams_template.html', context={'best_team_list': best_team_list,
                                                                                       'often_team_list': often_team_list,
                                                                                       'often_team_graph': often_team_graphic,
                                                                                       'winner_team_graph': winner_team_graphic
                                                                                        })