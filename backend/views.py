import ast
import json
from datetime import datetime

from django.shortcuts import render, render_to_response

from .sql_requests import *

CURRENT_YEAR_START = datetime.strptime('01/1/2020', '%m/%d/%Y').date()


# Create your views here.
def index(request, year=2020):
    total_players_per_year_list = get_total_players_per_year()
    years_dict = []
    for y in total_players_per_year_list:
        temp_dict = {
            'value': y[0],
            'year': int(y[1])
        }
        years_dict.append(temp_dict)
    json_players_per_year = ast.literal_eval(json.dumps(years_dict, ensure_ascii=False))

    total_teams_per_year_list = get_total_teams_per_year()
    years_dict = []
    for team in total_teams_per_year_list:
        temp_dict = {
            'value': team[0],
            'year': int(team[1])
        }
        years_dict.append(temp_dict)
    json_teams_per_year = ast.literal_eval(json.dumps(years_dict, ensure_ascii=False))

    total_teams_per_month_list = get_total_teams_per_month(year)
    month_dict = []
    for team in total_teams_per_month_list:
        temp_dict = {
            'value': team[0],
            'month': int(team[1])
        }
        month_dict.append(temp_dict)
    json_teams_per_month = ast.literal_eval(json.dumps(month_dict, ensure_ascii=False))

    total_players_per_month_list = get_total_players_per_month(year)
    month_dict = []
    for y in total_players_per_month_list:
        temp_dict = {
            'value': y[0],
            'year': int(y[1])
        }
        month_dict.append(temp_dict)
    json_players_per_month = ast.literal_eval(json.dumps(month_dict, ensure_ascii=False))

    total_teams_per_game_list = get_total_teams_per_game(year)
    games_dict = []
    for game in total_teams_per_game_list:
        temp_dict = {
            'name': game[0],
            'value': int(game[1])
        }
        games_dict.append(temp_dict)
    json_teams_per_game = ast.literal_eval(json.dumps(games_dict, ensure_ascii=False))

    total_players_per_game_list = get_total_players_per_game(year)
    games_dict = []
    for game in total_players_per_game_list:
        temp_dict = {
            'name': game[0],
            'value': int(game[1])
        }
        games_dict.append(temp_dict)
    json_players_per_game = ast.literal_eval(json.dumps(games_dict, ensure_ascii=False))

    forum_resonance_list = get_top_forum_resonance(year)[:30]
    games_dict = []
    for game in forum_resonance_list:
        temp_dict = {
            'name': game[0],
            'value': int(game[1])
        }
        games_dict.append(temp_dict)
    json_forum_resonance = ast.literal_eval(json.dumps(games_dict, ensure_ascii=False))

    quality_game_list = get_top_game_quality(year)[:40]
    games_dict = []
    for game in quality_game_list:
        temp_dict = {
            'name': game[0],
            # без str, highchart вместо точек ставит запятые и принимает десятичное число за два целых
            'value': str(game[1])
        }
        games_dict.append(temp_dict)
    json_quality_game_list = ast.literal_eval(json.dumps(games_dict, ensure_ascii=False))

    frequency_player_list = get_often_player_list(year)[:50]
    players_dict = []
    for player in frequency_player_list:
        temp_dict = {
            'name': player[0],
            'value': int(player[1])
        }
        players_dict.append(temp_dict)
    json_frequency_player_list = ast.literal_eval(json.dumps(players_dict, ensure_ascii=False))

    authors_and_games_list = get_all_authors_and_count_game(year)
    authors_dict = []
    for author in authors_and_games_list:
        temp_dict = {
            'name': author[0],
            'value': author[1]
        }
        authors_dict.append(temp_dict)
    json_authors_and_games_list = ast.literal_eval(json.dumps(authors_dict, ensure_ascii=False))

    best_team_list = get_best_team_list(year)
    teams_dict = []
    for team in best_team_list:
        temp_dict = {
            'name': team[0],
            'value': team[1]
        }
        teams_dict.append(temp_dict)
    json_winners = ast.literal_eval(json.dumps(teams_dict, ensure_ascii=False))

    frequency_team_list = get_often_team(year)[:20]
    often_dict = []
    for team in frequency_team_list:
        temp_dict = {
            'name': team[0],
            'url': team[1],
            'value': team[2]
        }
        often_dict.append(temp_dict)
    json_frequency_teams = ast.literal_eval(json.dumps(often_dict, ensure_ascii=False))

    authors_games_dict = get_author_and_his_games(year)
    often_players_table = get_often_player_list(year)
    rate_list = get_players_rate_list(year)
    often_teams_list = get_often_team(year)
    best_team_list = get_best_team_list(year)

    codes_count = get_code_count(year)
    correct_codes = get_correct_code_count(year)
    wrong_codes = get_wrong_code_count(year)
    code_with_wrong_address_all = wrong_address_all_time
    code_with_wrong_address_2020 = wrong_address_2020

    return render(request, 'backend/index.html', {'total_players_per_year': json_players_per_year,
                                                  'total_teams_per_year': json_teams_per_year,
                                                  'total_teams_per_month': json_teams_per_month,
                                                  'total_players_per_month': json_players_per_month,
                                                  'total_teams_per_game': json_teams_per_game,
                                                  'total_players_per_game': json_players_per_game,
                                                  'top_forum_resonance_game': json_forum_resonance,
                                                  'quality_game_list': json_quality_game_list,
                                                  'frequency_player_list': json_frequency_player_list,
                                                  'authors_and_games': json_authors_and_games_list,
                                                  'authors_dict': authors_games_dict,

                                                  'often_players_table': often_players_table,
                                                  'rate_list': rate_list,
                                                  'often_teams_list': often_teams_list,
                                                  'winner_list': best_team_list,

                                                  'codes_count': codes_count,
                                                  'correct_codes': correct_codes,
                                                  'wrong_codes': wrong_codes,
                                                  'wrong_address_all_time': code_with_wrong_address_all,
                                                  'wrong_address_2020': code_with_wrong_address_2020,

                                                  'total_win_per_team': json_winners,
                                                  'frequency_teams': json_frequency_teams,
                                                  'year': year,
                                                  })


def get_main_count_information(request):
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


def get_main_top_information(request):
    year = int(request.GET.get('year'))
    max_resonance_game = get_top_forum_resonance(year)[:3]
    max_quality_game =  get_top_game_quality(year)[:3]

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


def get_main_players_information(request):
    year = int(request.GET.get('year'))
    often_player_list = get_often_player_list(year)
    often_players = often_player_list[:5]

    rate_list = get_players_rate_list(year)
    good_rate_players = rate_list[:5]
    strict_rate_players = list(reversed(rate_list[-5:]))
    return render_to_response('backend/main_players_information_template.html', context={'good_rate_players': good_rate_players,
                                                                                        'strict_rate_players': strict_rate_players,
                                                                                        'often_players': often_players
                                                                                        })


