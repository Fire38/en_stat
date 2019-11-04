from django.db import connection
from .models import *


def get_games_count(year):
    """ Общее количество игр начиная с определенного года"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM backend_Game WHERE backend_Game.finish_date >= '01-01-%s'", [year])
        games_count = cursor.fetchone()[0]
    return games_count


def get_authors_count(year):
    """ Общее количество авторов начиная с определенного года"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT (DISTINCT backend_player.name) FROM backend_player, backend_author, backend_game WHERE"
                       " backend_player.id = backend_author.player_id AND backend_author.game_id = backend_game.id "
                       " AND backend_game.finish_date >= '01-01-%s'", [year])
        authors_count = cursor.fetchone()[0]
    return authors_count


def get_players_count(year):
    """ Общее количество игроков начиная с определенного года """
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT (DISTINCT backend_player.name) FROM backend_player, backend_game, backend_personal_statistic"
                              " WHERE backend_player.id = backend_personal_statistic.player_id AND "
                              " backend_game.id = backend_personal_statistic.game_id AND "
                              " backend_game.finish_date >= '01-01-%s'", [year])
        players_count = cursor.fetchone()[0]
    return players_count


def get_teams_count(year):
    """ Общее количество команд начиная с опр года"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(DISTINCT backend_team.name) FROM backend_game, backend_team, backend_game_team"
                       " WHERE backend_game.id=backend_game_team.game_id"
                       " AND backend_game_team.team_id=backend_team.id"
                       " AND backend_game.game_type = 'Командная'"
                       " AND backend_game.finish_date >= '01-01-%s'", [year])
        teams_count = cursor.fetchone()[0]
    return teams_count


def get_max_forum_resonance(year):
    """ Игра с максимальным количеством сообщений на форуме """
    with connection.cursor() as cursor:
        cursor.execute("SELECT name, url, forum_resonance FROM backend_game WHERE forum_resonance = (SELECT MAX(forum_resonance)"
                       " FROM backend_game WHERE backend_game.finish_date >= '01-01-%s')", [year])

        max_resonance_game = cursor.fetchone()
        # TODO ПОЛУЧИТЬ АВТОРА ИГРЫ  И СПИСОК ВСЕХ ИГР
    return max_resonance_game


def get_top_forum_resonance(year):
    """ Топ резонансных на форуме игр"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT name, forum_resonance FROM backend_game WHERE backend_game.finish_date >= '01-01-%s'"
                       " ORDER BY forum_resonance DESC", [year])
        top_forum_resonance = cursor.fetchall()
    return top_forum_resonance


def get_best_game_quality(year):
    """ Игра с максимальный коэфициентом качества"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT name, url, quality_index FROM backend_game WHERE quality_index = ( SELECT MAX(quality_index)"
                       " FROM backend_game WHERE backend_game.game_type = 'Командная' AND backend_game.finish_date >= '01-01-%s)')", [year])

        max_quality_game = cursor.fetchone()
        #print(max_quality_game)
    return max_quality_game


def get_top_game_quality(year):
    """ Топ игр по качеству"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT name, quality_index FROM backend_game WHERE game_type='Командная'"
                       " AND finish_date >= '01-01-%s' ORDER BY quality_index DESC", [year])
        top_game_quality = cursor.fetchall()
    # print(top_game_quality)
    return top_game_quality


def get_best_team(year):
    """ Самая побеждающая команда """
    with connection.cursor() as cursor:
        cursor.execute("SELECT backend_team.name, COUNT(backend_team.name) from backend_team, backend_game"
                       " WHERE  backend_game.winner = backend_team.name AND backend_game.finish_date >= '01-01-%s'"
                       " GROUP BY backend_team.name ORDER BY count DESC LIMIT 1", [year])
        best_team = cursor.fetchone()
    return best_team


def get_top_best_team(year):
    """ Топ команд по победам """
    with connection.cursor() as cursor:
        cursor.execute("SELECT backend_team.name, COUNT(backend_team.name) FROM backend_team, backend_game "
                       " WHERE backend_game.winner = backend_team.name AND backend_game.finish_date >= '01-01-%s'"
                       " GROUP BY backend_team.name", [year])
        winners_list = cursor.fetchall()
    return winners_list


def get_code_count(year):
    """ Число вбитых кодов за год """
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(backend_code.code_text) FROM backend_code, backend_code_game, backend_game"
                       " WHERE backend_game.id = backend_code_game.game_id AND backend_code_game.code_id=backend_code.id"
                       " AND backend_game.finish_date >= '01-01-%s'", [year])
        codes_count = cursor.fetchone()
    return codes_count


def get_author(year):
    """ Автор с большим количеством игр """
    with connection.cursor() as cursor:
        cursor.execute("SELECT backend_player.name, COUNT(backend_player.name) FROM backend_author, backend_player, "
                       " backend_game WHERE backend_player.id = backend_author.player_id AND "
                       " backend_author.game_id = backend_game.id AND backend_game.finish_date >= '01-01-%s' "
                       " GROUP BY backend_player.name ORDER BY count DESC LIMIT 1", [year])
        best_author = cursor.fetchone()
    return best_author


def get_all_authors_and_game(year):
    """ Все авторы и количество их игр """
    with connection.cursor() as cursor:
        cursor.execute("SELECT backend_player.name, COUNT(backend_player.name) FROM backend_author, backend_player, "
                       " backend_game WHERE backend_player.id = backend_author.player_id AND "
                       " backend_author.game_id = backend_game.id AND backend_game.finish_date >= '01-01-%s' "
                       " GROUP BY backend_player.name ORDER BY count DESC ", [year])
        author_and_game_count_list = cursor.fetchall()
    return author_and_game_count_list


def get_author_and_his_games(year):
    """ Все авторы и их игры """
    with connection.cursor() as cursor:
        cursor.execute("SELECT backend_player.name, backend_game.name, backend_game.url FROM backend_author, backend_player, "
                       " backend_game WHERE backend_player.id = backend_author.player_id AND "
                       " backend_author.game_id = backend_game.id AND backend_game.finish_date >= '01-01-%s' "
                       " GROUP BY backend_player.name, backend_game.name, backend_game.url ORDER BY backend_player.name", [year])
        authors_list_with_games = cursor.fetchall()

        authors_dict = {}
        authors =[]
        for i in authors_list_with_games:
            authors.append(i[0])
        authors_set = set(authors)

        for author in authors_set:
            games = []

            for record in authors_list_with_games:
                if author == record[0]:
                    games.append((record[1], record[2]))
                    authors_dict[author] = games

    return  authors_dict


def get_often_player(year):
    """ Самый частоиграющий игрок """
    with connection.cursor() as cursor:
        cursor.execute("SELECT backend_player.name, count(backend_player.name)"
                       " FROM backend_personal_statistic, backend_game, backend_player"
                       " WHERE backend_game.id=backend_personal_statistic.game_id"
                       " AND backend_game.finish_date >= '01-01-%s'"
                       " AND backend_personal_statistic.player_id = backend_player.id"
                       " GROUP BY backend_player.name"
                       " ORDER BY count DESC LIMIT 1", [year])
        often_player = cursor.fetchone()
    return often_player


def get_often_player_list(year):
    """ Топ частоиграющих игроков """
    with connection.cursor() as cursor:
        cursor.execute("SELECT backend_player.name, count(backend_player.name)"
                       " FROM backend_personal_statistic, backend_game, backend_player"
                       " WHERE backend_game.id=backend_personal_statistic.game_id"
                       " AND backend_game.finish_date >= '01-01-%s'"
                       " AND backend_personal_statistic.player_id = backend_player.id"
                       " GROUP BY backend_player.name"
                       " ORDER BY count DESC", [year])
        often_player_list = cursor.fetchall()
    return often_player_list


def get_often_team(year):
    """ Самая частоиграющая команда """
    with connection.cursor() as cursor:
        cursor.execute("SELECT backend_team.name, backend_team.url, COUNT(backend_team.name) FROM backend_team, backend_game,"
                       " backend_game_team WHERE backend_team.id=backend_game_team.team_id"
                       " AND  backend_game_team.game_id=backend_game.id"
                       " AND backend_game.finish_date >= '01-01-%s'"
                       " AND backend_game.game_type='Командная'"
                       " GROUP BY backend_team.name, backend_team.url"
                       " ORDER BY COUNT(backend_team.name) DESC LIMIT 1", [year])
        often_team = cursor.fetchone()
        print(often_team)
    return often_team






# TODO добавить в каждый запрос что игра командная!
"""
кто чаще всего играет
select backend_player.name, count(backend_player.name) from backend_personal_statistic, backend_game, backend_player where backend_game.id=backend_personal_statistic.game_id AND backend_game.finish_date >= '01-01-2017' and backend_personal_statistic.player_id = backend_player.id group by backend_player.name order by count DESC;

"""

def get_game_per_month(year):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name, fin")


"""
рейтинг игр 
select name, url, MAX(quality_index) from backend_game where backend_game.finish_date >= '01-01-2019' 
AND backend_game.game_type='Командная' group by quality_index, name, url order by quality_index;


количество кодов за год
SELECT backend_code.code_text, backend_game.name FROM backend_code, backend_game, backend_code_game  
WHERE backend_code_game.game_id = backend_game.id AND backend_game.finish_date >= '01-01-2019' AND backend_code.id = backend_code_game.code_id;

"""
