from django.db import connection

# TODO переделать самый кто-то нибудь если выдаст двух игроков с одинаковым количеством??


def get_games_count(year):
    """ Общее количество игр начиная с определенного года"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM backend_Game WHERE backend_Game.finish_date >= '01-01-%s'", [year])
        games_count = cursor.fetchone()[0]
    return games_count


def get_authors_count(year):
    """ Общее количество авторов начиная с определенного года"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(DISTINCT backend_player.name) FROM backend_player"
                       " JOIN backend_author ON backend_player.id=backend_author.player_id"
                       " JOIN backend_game ON backend_game.id=backend_author.game_id"
                       " WHERE backend_game.finish_date >= '01-01-%s'", [year])
        authors_count = cursor.fetchone()[0]
    return authors_count


def get_all_authors_and_count_game(year):
    """ Все авторы и количество их игр """
    with connection.cursor() as cursor:
        cursor.execute("SELECT backend_player.name, COUNT(backend_player.name) FROM backend_author"
                       " JOIN backend_player ON backend_player.id=backend_author.player_id"
                       " JOIN backend_game ON backend_game.id=backend_author.game_id"
                       " WHERE backend_game.finish_date >= '01-01-%s' GROUP BY backend_player.name"
                       " ORDER BY COUNT(backend_player.name) DESC", [year])
        author_and_game_count_list = cursor.fetchall()
    return author_and_game_count_list


def get_author_and_his_games(year):
    """ Все авторы и их игры """
    with connection.cursor() as cursor:
        cursor.execute("SELECT backend_player.name, backend_game.name, backend_game.url FROM backend_author"
                       " JOIN backend_player ON backend_author.player_id=backend_player.id"
                       " JOIN backend_game ON backend_game.id=backend_author.game_id"
                       " WHERE backend_game.finish_date >= '01-01-%s'"
                       " GROUP BY backend_player.name, backend_game.name, backend_game.url"
                       " ORDER BY backend_player.name", [year])
        authors_list_with_games = cursor.fetchall()

        authors_dict = {}
        authors = []
        for i in authors_list_with_games:
            authors.append(i[0])
        authors_set = set(authors)

        for author in authors_set:
            games = []

            for record in authors_list_with_games:
                if author == record[0]:
                    games.append((record[1], record[2]))
                    authors_dict[author] = games
    return authors_dict


def get_players_count(year):
    """ Общее количество игроков начиная с определенного года """
    with connection.cursor() as cursor:
        cursor.execute("SELECT count(distinct backend_player.name) FROM backend_player"
                       " JOIN backend_personal_statistic ON backend_player.id=backend_personal_statistic.player_id"
                       " JOIN backend_game ON backend_personal_statistic.game_id=backend_game.id"
                       " WHERE backend_game.finish_date >= '01-01-%s'", [year])
        players_count = cursor.fetchone()[0]
    return players_count


def get_total_players_per_year():
    """Общее количество игроков по годам"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(DISTINCT backend_player.name), EXTRACT(year FROM finish_date) FROM backend_player"
                       " JOIN backend_personal_statistic ON backend_player.id=backend_personal_statistic.player_id"
                       " JOIN backend_game ON backend_personal_statistic.game_id=backend_game.id"
                       " GROUP BY EXTRACT(year FROM backend_game.finish_date)")
        total_players_per_year = cursor.fetchall()
    return total_players_per_year


def get_total_players_per_month(year):
    """Общее количество игроков по месяцам года"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(DISTINCT backend_player.name), EXTRACT(month FROM finish_date) FROM backend_player"
                       " JOIN backend_personal_statistic ON backend_player.id=backend_personal_statistic.player_id"
                       " JOIN backend_game ON backend_personal_statistic.game_id=backend_game.id"
                       " WHERE EXTRACT(year FROM backend_game.finish_date) = '%s' "
                       " GROUP BY EXTRACT(month FROM backend_game.finish_date)", [year])
        total_players_per_month = cursor.fetchall()
    return total_players_per_month


def get_total_players_per_game(year):
    """Общее количество игроков по играм"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT backend_game.name, COUNT(backend_player.name) "
                       " FROM backend_personal_statistic "
                       " JOIN backend_player on backend_personal_statistic.player_id = backend_player.id"
                       " JOIN backend_game ON backend_game.id=backend_personal_statistic.game_id"
                       " WHERE EXTRACT(year FROM backend_game.finish_date) = '%s'"
                       " AND backend_game.game_type = 'Командная' "
                       " GROUP BY backend_game.name"
                       " ORDER BY COUNT(backend_player) DESC", [year])
        total_players_per_game = cursor.fetchall()
    return total_players_per_game


def get_teams_count(year):
    """ Общее количество команд начиная с опр года"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(DISTINCT backend_team.name) FROM backend_game"
                       " JOIN backend_game_team ON backend_game.id=backend_game_team.game_id"
                       " JOIN backend_team ON backend_game_team.team_id=backend_team.id"
                       " WHERE backend_game.game_type='Командная'"
                       " AND backend_game.finish_date >= '01-01-%s'", [year])
        teams_count = cursor.fetchone()[0]
    return teams_count


def get_total_teams_per_year():
    """Общее количество команд по годам"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(DISTINCT backend_team.name), EXTRACT(year FROM finish_date) FROM backend_game"
                       " JOIN backend_game_team ON backend_game.id=backend_game_team.game_id"
                       " JOIN backend_team ON backend_game_team.team_id=backend_team.id"
                       " WHERE backend_game.game_type='Командная'"
                       " GROUP BY EXTRACT(year FROM backend_game.finish_date)")
        total_teams_per_year = cursor.fetchall()
    return total_teams_per_year


def get_total_teams_per_month(year):
    """Общее количество команд по месяцам года"""
    with connection.cursor() as cursor:
         cursor.execute("SELECT COUNT(DISTINCT backend_team.name), EXTRACT(month FROM finish_date) FROM backend_game"
                        " JOIN backend_game_team ON backend_game.id=backend_game_team.game_id"
                        " JOIN backend_team ON backend_game_team.team_id=backend_team.id"
                        " WHERE backend_game.game_type='Командная'"
                        " AND EXTRACT(year FROM backend_game.finish_date) = '%s'"
                        " GROUP BY EXTRACT(month FROM backend_game.finish_date)", [year])
         total_teams_per_month = cursor.fetchall()
    return total_teams_per_month


def get_total_teams_per_game(year):
    """Общее количество команд по играм"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT backend_game.name, COUNT(backend_team.name) FROM backend_team"
                       " JOIN backend_game_team ON backend_team.id=backend_game_team.team_id "
                       " JOIN backend_game ON backend_game.id=backend_game_team.game_id"
                       " WHERE EXTRACT(year FROM backend_game.finish_date) = '%s'"
                       " AND backend_game.game_type='Командная' "
                       " GROUP BY backend_game.name "
                       " ORDER BY count(backend_team.name) DESC", [year])
        total_teams_per_game = cursor.fetchall()
    return total_teams_per_game


def get_max_forum_resonance(year):
    """ Игра с максимальным количеством сообщений на форуме """
    with connection.cursor() as cursor:
        print(year)

        cursor.execute("SELECT name, url, forum_resonance FROM backend_game"
                       " WHERE forum_resonance=(SELECT MAX(forum_resonance) "
                       "                        FROM backend_game "
                       "                        WHERE finish_date >= '01-01-%s') "
                       " AND finish_date >= '01-01-%s'", [year, year])
        max_resonance_game = cursor.fetchall()
    return max_resonance_game


def get_top_forum_resonance(year):
    """ Список резонансных на форуме игр"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT name, forum_resonance, url FROM backend_game WHERE backend_game.finish_date >= '01-01-%s'"
                       " ORDER BY forum_resonance DESC", [year])
        top_forum_resonance = cursor.fetchall()
    return top_forum_resonance


def get_best_game_quality(year):
    """ Игра с максимальный коэфициентом качества"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT name, url, quality_index FROM backend_game "
                       " WHERE quality_index = (SELECT MAX(quality_index) FROM backend_game "
                       "                        WHERE backend_game.game_type = 'Командная' "
                       "                        AND backend_game.finish_date >= '01-01-%s') "
                       "AND finish_date >= '01-01-%s'", [year, year])

        max_quality_game = cursor.fetchall()
    return max_quality_game


def get_top_game_quality(year):
    """ Список игр по качеству"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT name, quality_index, url FROM backend_game"
                       " WHERE game_type='Командная'"
                       " AND finish_date >= '01-01-%s' "
                       " ORDER BY quality_index DESC", [year])
        top_game_quality = cursor.fetchall()
    # print(top_game_quality)
    return top_game_quality


def get_best_team_list(year):
    """ Топ команд по победам """
    with connection.cursor() as cursor:
        cursor.execute("SELECT backend_team.name, COUNT(backend_team.name)"
                       " FROM backend_team JOIN backend_game ON backend_game.winner = backend_team.name"
                       " WHERE backend_game.finish_date >= '01-01-%s'"
                       " GROUP BY backend_team.name"
                       " ORDER BY COUNT DESC", [year])
        winners_list = cursor.fetchall()
    return winners_list


def get_often_team(year):
    """ Самая частоиграющая команда """
    with connection.cursor() as cursor:
        cursor.execute("SELECT backend_team.name, backend_team.url, COUNT(backend_team.name) FROM backend_team"
                       " JOIN backend_game_team ON backend_team.id=backend_game_team.team_id"
                       " JOIN backend_game ON backend_game_team.game_id=backend_game.id"
                       " WHERE backend_game.finish_date >= '01-01-%s'"
                       " AND backend_game.game_type='Командная'"
                       " GROUP BY backend_team.name, backend_team.url"
                       " ORDER BY COUNT(backend_team.name) DESC", [year])
        often_team = cursor.fetchall()
    return often_team


def get_players_rate_list(year):
    """ Список средних оценок игроков """
    with connection.cursor() as cursor:
        cursor.execute("SELECT backend_player.name, COUNT(backend_player.name), ROUND(AVG(backend_rating.rate),4) "
                       " FROM backend_player "
                       " JOIN backend_rating ON backend_player.id=backend_rating.player_id "
                       " JOIN backend_game ON backend_game.id = backend_rating.game_id  "
                       " WHERE backend_game.finish_date >= '01-01-%s' "
                       " GROUP BY backend_player.name "
                       " HAVING COUNT(backend_player.name) > 5 "
                       " ORDER BY ROUND DESC", [year])
        rate_list = cursor.fetchall()
    return rate_list


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
                       " HAVING COUNT(backend_player.name) > 1"
                       " ORDER BY count DESC", [year])
        often_player_list = cursor.fetchall()
    return often_player_list


def get_code_count(year):
    """ Число вбитых кодов  """
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(backend_code.code_text) FROM backend_code, backend_code_game, backend_game"
                       " WHERE backend_game.id = backend_code_game.game_id AND backend_code_game.code_id=backend_code.id"
                       " AND backend_game.finish_date >= '01-01-%s'", [year])
        codes_count = cursor.fetchone()
    return codes_count


def get_correct_code_count(year):
    """ Чисто верных вбитий """
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) from backend_code"
                       " JOIN backend_code_game ON backend_code_game.code_id = backend_code.id"
                       " JOIN backend_game on backend_game.id = backend_code_game.game_id"
                       " WHERE backend_game.finish_date >= '01-01-%s'"
                       " AND backend_code.correct = true", [year])
        correct_codes_count = cursor.fetchone()
    return correct_codes_count


def get_wrong_code_count(year):
    """ Число неверных вбитий """
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) from backend_code"
                       " JOIN backend_code_game ON backend_code_game.code_id = backend_code.id"
                       " JOIN backend_game on backend_game.id = backend_code_game.game_id"
                       " WHERE backend_game.finish_date >= '01-01-%s'"
                       " AND backend_code.correct = false", [year])
        wrong_codes_count = cursor.fetchone()
    return wrong_codes_count


wrong_address_all_time = [
    {'name': 'Янгеля 120', 'value': 280},
    {'name': 'Маршала Жукова 7', 'value': 194},
    {'name': 'Обручева 28', 'value': 166},
    {'name': 'Крупской 56', 'value': 152},
    {'name': 'Янгеля 122', 'value': 129},
    {'name': 'Советская 7', 'value': 101},
    {'name': 'Южная 20', 'value': 92},
    {'name': 'Подбельского 36', 'value': 92},
    {'name': 'Южная 12', 'value': 91},
    {'name': 'Южная 8', 'value': 89}
]


wrong_address_2019 = [
    {'name': 'Янгеля 120', 'value': 66},
    {'name': 'Обручева 28', 'value': 49},
    {'name': 'Янгеля 122', 'value': 37},
    {'name': 'Советская 29', 'value': 30},
    {'name': 'Крупской 40', 'value': 29},
    {'name': 'Крупской 56', 'value': 27},
    {'name': 'Кирова 12', 'value': 25},
    {'name': 'Советская 34', 'value': 24},
    {'name': 'Советская 15', 'value': 23},
    {'name': 'Маршала Жукова 7', 'value': 23},
]



def game_count_for_uniq_code(year):
    """ Возвращает количество игр в которых встречался каждый верный код"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT backend_code.code_text, COUNT(DISTINCT backend_code_game.game_id) "
                       " filter (WHERE backend_code.correct) game_count FROM backend_code_game"
                       " INNER JOIN backend_code ON backend_code.id=backend_code_game.code_id"
                       " JOIN backend_game on backend_game.id = backend_code_game.game_id"
                       " WHERE backend_game.finish_date >= '01-01-1999'"
                       " GROUP BY backend_code.code_text"
                       " ORDER BY game_count DESC")
        game_count = cursor.fetchone()
        """ Или на джанге
        qs = Code.game.through.objects.filter(code__correct=True).values('code__code_text', 'game').distinct().values(
            'code__code_text').order_by().annotate(count=Count('game', distinct=True))"""
    return game_count
