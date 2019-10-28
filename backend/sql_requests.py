from django.db import connection
from .models import *


def get_count(year):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM backend_Game WHERE backend_Game.finish_date >= '01-01-%s'", [year])
        games_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (DISTINCT backend_player.name) FROM backend_player, backend_author, backend_game WHERE"
                       " backend_player.id = backend_author.player_id AND backend_author.game_id = backend_game.id "
                       " AND backend_game.finish_date >= '01-01-%s'", [year])
        authors_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (DISTINCT backend_player.name) FROM backend_player, backend_game, backend_personal_statistic"
                              " WHERE backend_player.id = backend_personal_statistic.player_id AND "
                              " backend_game.id = backend_personal_statistic.game_id AND "
                              " backend_game.finish_date >= '01-01-%s'", [year])
        players_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (DISTINCT backend_team.name) FROM backend_team, backend_game, "
                       " backend_personal_statistic WHERE backend_team.id = backend_personal_statistic.team_id AND"
                       " backend_personal_statistic.game_id = backend_game.id "
                       " AND backend_game.finish_date >= '01-01-%s'", [year])
        teams_count = cursor.fetchone()[0]

    return games_count, authors_count, players_count, teams_count


def get_resonance(year):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name, url, forum_resonance FROM backend_game WHERE forum_resonance = (SELECT MAX(forum_resonance)"
                       " FROM backend_game WHERE backend_game.finish_date >= '01-01-%s')", [year])

        max_resonance_game = cursor.fetchone()
        # TODO ПОЛУЧИТЬ АВТОРА ИГРЫ  И СПИСОК ВСЕХ ИГР
    return max_resonance_game

def get_game_quality(year):
     with connection.cursor() as cursor:
        cursor.execute("SELECT name, url, quality_index FROM backend_game WHERE quality_index = ( SELECT MAX(quality_index)"
                       " FROM backend_game WHERE backend_game.game_type = 'Командная' AND backend_game.finish_date >= '01-01-%s)')", [year])

        max_quality_game = cursor.fetchone()
        print(max_quality_game)


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
