from django.db import connection
from .models import *

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
        cursor.execute("SELECT name, quality_index FROM backend_game WHERE game_type='Командная'"
                       " AND finish_date >= '01-01-%s' ORDER BY quality_index DESC", [year])
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



from .models import *
from django.db.models import Q
def test_function():

    test_dict ={}

    all_codes = Code.objects.filter(Q(game__finish_date__gte='1999-01-01')&Q(correct=True)).values('code_text').distinct()
    for i, code in enumerate(all_codes):
        print("Код номер ", i)
        test_dict[code['code_text']] = 0
        for game in Game.objects.filter(finish_date__gte='2019-01-01'):
            # print('поменяли игру')
            # print(game)
            for game_code in game.code_set.filter(correct=True):
                # print(code['code_text'], game_code.code_text)
                if code['code_text'] == game_code.code_text:
                    print('Зачет')
                    test_dict[code['code_text']] += 1
                    print(test_dict)
                    break

    print(test_dict)
    return test_dict


dd = {'красотень': 0, '69ограбление': 0, 'комната': 0, 'фикус': 1, 'wewanttokillemall': 0, '14893': 0, 'ася': 0, 'монета': 2, 'хищник': 0, 'козёл': 0, 'танк пора': 0, '9224': 0, 'энгельса': 0, '1414 недель тишины': 0, 'hna05': 0, 'грешник': 0, '784430': 0, 'квин': 0, 'ботинки': 0, '64дверь': 0, 'нычка': 0, 'жёсткость': 1, 'жесть': 0, 'кран': 3, 'мало': 0, 'вариоусартистс': 0, 'леонард': 0, 'ой': 0, 'харальд вангер': 0, '144красное на черном': 0, 'bagamol': 1, 'ап': 0, 'онопко': 0, '27-69-31': 0, 'веретено': 1, 'медельин': 0, 'пробельгия': 0, 'пинки': 0, 'подруженька': 0, 'индустриальный 4б': 1, 'кемерово': 0, 'полынь, опиум': 0, 'ресурсообеспеченность': 0, 'флот': 0, 'грехов': 0, 'отбросы': 0, 'араз': 0, 'труп38': 0, 'арканзас': 0, 'пляж': 1, 'брикет крикет': 1, '21 марта': 0, '453148': 0, 'дебют': 1, 'сэмюэл л. джексон': 0, 'каторга': 0, 'парк паук': 1, 'сайракс': 0, 'энка': 1, 'рубака': 0, 'вперед321': 1, '259050': 0, 'вар': 1, 'вассермантия': 0, 'детройт': 0, 'тетраклерик': 0, 'восклицательный': 0, 'качели': 1, '99девушка по городу': 0, 'ливанов зеленая соломин': 0, 'хуй3': 0, 'баланда': 0, 'забрало': 0, 'завал зачета': 1, '1717': 0, 'анка': 0, 'г17': 0, 'гекконтики': 0, 'пирамида хеопса': 0, 'доллар': 0, '131': 0, 'изцентра': 0, 'гамлет': 0, 'творительный': 0, 'аегис': 0, '034маккартни': 0, '444452': 0, 'зевота': 0, 'наут': 0, 'пчела': 0, 'груд': 0, 'опус': 0, 'фригг': 0, 'пиар': 0, 'советская 12а': 1, 'квенья': 0, 'радиус420': 1, 'пень': 0, 'рядовое событие': 1, 'бондиана': 1, 'изображение': 1, 'сороктри': 0, 'моргалы': 0, 'германия': 0, 'кинг': 0, 'иждивенец': 0, 'гайка майка': 1, 'муж': 0, 'мунген': 0, 'лоботрясы': 0, 'лучик': 0, 'сильвер': 0, 'покосбык': 0, 'nikolaus': 0, 'дверь': 0, '1328': 0, 'колоннада': 0, 'ленина, 42': 0, 'центнерка': 0, 'фелпс': 0, 'куб': 0, '5124': 1, 'ix7gs': 0, '345727': 0, 'lost': 0, 'свидригайло': 0, '18,00': 0, 'бостон': 1, 'лето': 0, 'гагарина 45': 0, 'marvel': 0, '1909 1912': 1, 'корвет': 0, 'фиалок': 0, 'частотаhz': 0, 'де вито': 0, 'бульвар победы, 18': 0, 'мысли': 0, 'пекло': 0, 'марвин': 0, 'лун': 0, '428866': 0, 'барт': 0, 'маршрутная сеть': 1, 'стоит': 0, 'золото': 0, 'лицо2': 0, 'развалина': 0, 'анк-морпорк': 0, 'бгеикнопрсчъь': 1, 'ковер-вертолет': 0, '5566': 0, 'укладчик': 0, 'ч': 0, 'римский': 0, 'комбат вомбат': 1, '39-05-38': 0, 'мимикар': 0, '310310': 1, 'ляпис': 0, 'артист': 0, 'янгеля 111а': 0, '3771': 0, 'молекула': 0, 'рак': 0, 'гипопатам': 0, 'маркса': 0}

def dict_sort(d):
    list_d = list(d.items())

    list_d.sort(key=lambda i: i[1])
    return list_d


# TODO добавить в каждый запрос что игра командная!
"""
кто чаще всего играет
select backend_player.name, count(backend_player.name) from backend_personal_statistic, backend_game, backend_player where backend_game.id=backend_personal_statistic.game_id AND backend_game.finish_date >= '01-01-2017' and backend_personal_statistic.player_id = backend_player.id group by backend_player.name order by count DESC;



количество кодов за год
SELECT backend_code.code_text, backend_game.name FROM backend_code, backend_game, backend_code_game  
WHERE backend_code_game.game_id = backend_game.id AND backend_game.finish_date >= '01-01-2019' AND backend_code.id = backend_code_game.code_id;

средняя оценка игрока
SELECT backend_player.name, AVG(backend_rating.rate) 
FROM backend_player JOIN backend_rating on backend_player.id=backend_rating.player_id group by backend_player.name order by avg;

"""



"""
все коды за год
SELECT backend_code.code_text, COUNT(backend_code.code_text)
FROM backend_code JOIN backend_code_game
ON backend_code.id = backend_code_game.code_id
JOIN backend_game ON backend_game.id = backend_code_game.game_id
WHERE backend_game.finish_date >= '01-01-2019'
GROUP BY backend_code.code_text
ORDER BY COUNT(backend_code.code_text) DESC;


"""




"""
SELECT backend_code.code_text, COUNT(backend_game.) 
FROM backend_code 
JOIN backend_code_game ON backend_code.id=backend_code_game.code_id 
JOIN backend_game ON backend_game.id=backend_code_game.game_id
WHERE 
backend_code.correct=true
AND 
backend_game.finish_date >= '01-01-2019'
AND 
backend_code.code_text IN 
    (
     SELECT DISTINCT backend_code.code_text 
     FROM backend_code 
     JOIN backend_code_game ON backend_code.id=backend_code_game.code_id
     JOIN backend_game ON backend_game.id=backend_code_game.game_id
     WHERE 
     backend_code.correct=true 
     AND 
     backend_game.finish_date >= '01-01-2019'
     )
GROUP BY backend_code.code_text 
ORDER BY COUNT(backend_game.name) 
DESC;


"""