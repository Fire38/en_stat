import re
import os
import pprint
import django
import requests
import datetime
from time import sleep
from random import randint
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "en_statistic.settings")
django.setup()

from backend.models import Game, Team, Player, Personal_statistic, Rating, Code, Author


LOGIN_URL = "http://vbratske.en.cx/Login.aspx"
LOGIN_DATA = {'Login': 'f1re', 'Password': 'Zte261192', 'socailAssign': '0', 'EnButton1': 'Sing In', 'ddlNetwork': '1', 'mobile': '0'}

MAIN_URL = "http://vbratske.en.cx"
ua = UserAgent(use_cache_server=True)
headers = {'User-Agent': ua.random}

# получаем токен, ид сессии
session = requests.Session()
res = session.get(LOGIN_URL, headers=headers)
print(res.cookies.get_dict())

data = {**LOGIN_DATA, **res.cookies.get_dict()}

res = session.post(LOGIN_URL, params=data, headers=headers, allow_redirects=False)
for i in res.history:
    print('tut')
    print(i.status_code, i.url)
#print(res.request.headers)

print(res.cookies.get_dict())




def get_domain_teams_list():
    """Все команды домена"""
    for i in range(1,10):
        url = "http://vbratske.en.cx/Teams/TeamList.aspx?page=" + str(i)
        rr = session.get(url, headers=headers)
        soup = BeautifulSoup(rr.text, 'html.parser')
        teams = soup.find_all(id=re.compile("_lnkTeamInfo"))
        for team in teams:
            print(team.text)
            Team.objects.get_or_create(name=team.text, url=MAIN_URL+team['href'])


def get_games_teams(soup, game_type):
    """Команды принимающие участие в конкретной игре"""
    print('\nИщем учавствующие команды: \n')
    teams = soup.find_all(id="lnkPlayerInfo")
    if game_type == 'Командная':
        for team in teams:
            print("В этой игре учавствовала команда: " + team.text)
            Team.objects.get_or_create(name=team.text, url=MAIN_URL+team['href'])
        return teams
    else:
        for team in teams:
            print("В этой игре учавствовал игрок: " + team.text)


def get_winner(soup, game_type):
    print(game_type)
    if game_type == 'Командная':
        winner = soup.find(id='top10Winners_SingleRepeater_ctl01_lnkWinnerInfo')
        print("Победитель: ", winner.text)
        return winner.text
    elif game_type == 'Одиночка на движке схватки':
        # TODO не ищет скотина
        """
        print(soup)
        winner = soup.find(id=re.compile("wetWarsTop10Winners_SingleRepeater_ctl01_lnkWinnerInfo"))
        print('PFFF', winner)"""
        winner = "Не команда"
    else:
        # если одиночка
        winner = soup.find(id="wetWarsTop10Winners_SingleRepeater_ctl01_lnkWinnerInfo")

        print("Победитель:", winner)
    return winner


def get_player_rate(soup):
    """Определяет какую оценку поставил игрок в конкретной игре"""
    try:
        full_teams_list = soup.find(id='lnkTopFull')
        res = session.get(MAIN_URL + full_teams_list['href'], headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
    except:
        pass

    rate_links = soup.find_all(id=re.compile('_TeamRateLink'))
    player_rate_dict = {}
    print("\nЗаписываем оценки игроков\n")
    for rate_link in rate_links:

        # страхуемся что никто в команде не поставил оценку
        try:
            res = session.get(MAIN_URL + rate_link['href'], headers=headers)
            # player_block = res.text.split('toWinnerItem')
            soup = BeautifulSoup(res.text, 'html.parser')
            player_lines = soup.find_all(class_='toWinnerItem')
            for line in player_lines:
                player = line.find(id=re.compile('_lnkUserInfo'))
                rate = line.find(class_=re.compile('topWinners pink'))
                player_rate_dict[player.text] = rate.text
                # print("ИГРОК", player.text, ' поставил оценку: ', rate.text)
        except:
            print("Без оценок")
    pprint.pprint(player_rate_dict)
    return player_rate_dict


def get_teams_players(soup):
    """Состав команды на конкретную игру"""
    print("\n Собираем информацию о составах команд\n")
    full_team_url = soup.find(id='lnkWinnerMembersEdit')

    res = session.get(MAIN_URL + full_team_url['href'], headers=headers)
    page_block = res.text.split('Team:')
    team_dict = {}
    for page in page_block:
        # print("БЛОК-------------------", page)
        soup = BeautifulSoup(page, 'html.parser')
        players = soup.find_all(id=re.compile("WinnersRepeater_ctl"))
        team_name = soup.find('span', class_='gold bold')
        print("Название команды", team_name)
        team = []
        for player in players:
            team.append(player)
        try:
            team_dict[team_name.text] = team
        except:
            pass
    return team_dict
        #print("------------------------\n")


def get_monitoring(soup):
    monitoring_href = soup.find(id='GameDetail_lnkMonitoring')
    res = session.get(MAIN_URL + monitoring_href['href'], headers=headers)
    page = BeautifulSoup(res.text, 'html.parser')
    pagintor = page.find_all('a', href=re.compile('Administration/Games/ActionMonitor.aspx\?gid='))
    last_page = pagintor[len(pagintor)-1].text
    i = 1

    code_list = []


    while i <= int(last_page):
        print(MAIN_URL + monitoring_href['href'] + '&page=' + str(i))
        res = session.get(MAIN_URL + monitoring_href['href'] + '&page=' + str(i), headers=headers)
        player_block = res.text.split('padL5')
        for block in player_block:
            soup = BeautifulSoup(block, 'html.parser')
            try:
                sublist = []
                # team = soup.find(id=re.compile('lnkTeam'))
                player = soup.find(id=re.compile('lnkUserInfo'))
                code_type = soup.find(id=re.compile('_lblCorrectValue'))
                #print("Родитель:", code_type.parent)
                #print("МЫ ТУТ",code_type.parent.findNext('td'), "\n")
                code_text = soup.find_all('span', class_='nonLatinChar')
                if code_text == []:
                    #print('TUT')
                    #print(code_type.parent.findNext('td').text)
                    code_text = code_type.parent.findNext('td').text
                    parent = code_text
                else:
                    parent = code_text[0].parent.text
                # print(player.text, code_type.text)
                """
                if len(code_text) > 1:
                    full_code = ''
                    for code in code_text:
                        full_code += code.text + ' '
                    print(full_code)
                else:
                    full_code = code_text[0].text
                    # print(one_code)
                    """
                sublist.append(player)
                sublist.append(code_type.text)
                sublist.append(parent)
                print("Строка мониторинга: ", sublist)
                code_list.append(sublist)
                # print(type(code_list))

            except:
                # print('tut')
                pass
        print('====================================================\n')
        i += 1
        sleep(randint(2,4))

    return code_list


def get_general_game_information(soup):
    game_title = soup.find(id='lnkGameTitle')
    # print(game_title)
    print('Название: ', game_title.text)

    #re потому что разные id
    authors = soup.find_all(id=re.compile("GameDetail_AuthorsRepeater_ct"))
    for author in authors:
        Player.objects.get_or_create(name=author.text, url=MAIN_URL + author['href'])
        print("Автор: " + author.text)

    game_diff = soup.find(id='GameDetail_lnkGameComplexity')
    print('Коэффициент сложности игры: ', game_diff.text)

    try:
        quality_index = soup.find(id='GameDetail_lnkGameQuality').text
        # ебаный пиздец если игра признана не состоявшейся, а потом произошел откат
        if quality_index == '-':
            print('НУ ЕБАНЫ В РОТ, ДЖОКЕР!')
            quality_index = 0.0
        print('Индекс качества игры: ', quality_index)
        game_type = 'Командная'
    except:
        quality_index = 0.0
        print(quality_index)
        game_type = 'Одиночная игра'

    #цепляемся за статистику, а в родительском элементе количество команд
    try:
        team_count = soup.find(id='GameDetail_lnkGameStat').parent.text
        if 'teams' in team_count:
            team_count = team_count.split(' ')[0].strip()
            team_count = team_count.replace(u'\xa0', u' ').split(' ')[0]
            print("Количество команд: ", team_count)
        else:
            game_type = "Одиночка на движке схватки"
            team_count = 0
            print("ОДИНОЧКА НА СХВАТКЕ")
    except:
        team_count = 0
        print('Одиночная игра')

    forum_resonance = soup.find(id='GameDetail_lnkGuestBook').text.split(' ')[0]
    print('Сообщений на форуме: ', forum_resonance)

    finish_date = soup.find(id='top10Winners_SingleRepeater_ctl01_TdWinDateTime')
    # TODO костыль с датами
    try:
        date = datetime.datetime.strptime(finish_date.text.split(' ')[0].strip(), '%m/%d/%Y') - datetime.timedelta(days=1)
        print(date)
    except:
        date = datetime.date(year=1999, month=1, day=1)

    return game_title, url, game_diff, quality_index, team_count, game_type, forum_resonance, date, authors


#get_domain_teams_list()
GAME_LIST_URL = "http://vbratske.en.cx/Games.aspx?page="
for i in range(1,25):
    print("СТРАНИЦА: ", i)
    rr = session.get(GAME_LIST_URL + str(i), headers=headers)

    soup = BeautifulSoup(rr.text, 'html.parser')
    game_list = []
    games = soup.find_all(id='lnkGameTitle')
    for game in games:
        game_list.append(game['href'])

    for game_href in game_list:
        url = 'http://vbratske.en.cx' + game_href
        print(url)
        res = session.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        game_title, url, game_diff, quality_index, team_count, game_type, forum_resonance, date, authors = get_general_game_information(soup)
        # если игра состоялась и индекс качества есть
        try:
            game = Game.objects.get_or_create(name=game_title.text,
                                              url=url,
                                              diff_game=game_diff.text,
                                              quality_index=quality_index,
                                              game_type=game_type,
                                              team_count=team_count,
                                              forum_resonance=forum_resonance,
                                              finish_date=date)[0]
            winner = get_winner(soup, game_type)
            game.winner = winner
            game.save()
            if game_type == 'Командная':
                # получаем команды, которые играли
                teams = get_games_teams(soup, game_type)
                for team in teams:
                    t = Team.objects.get_or_create(name=team.text)[0]
                    game.team.add(t)
                    game.save()
                # выясняем кто за кого играл
                # TODO какой игрок в какой команде был на какой игре
                playing_teams = get_teams_players(soup)
                for team_name, player_list in playing_teams.items():
                    team = Team.objects.get(name=team_name)
                    for player in player_list:
                        player = Player.objects.get_or_create(name=player.text, url = MAIN_URL + player['href'])[0]
                        Personal_statistic.objects.get_or_create(player=player, game=game, team=team)
                # получаем оценки игроков за игру
                rate_dict = get_player_rate(soup)
                for player_name, rate in rate_dict.items():
                    player = Player.objects.get(name=player_name)
                    Rating.objects.get_or_create(player=player, game=game, rate=rate)

                # если мониторинг открыт
                try:
                    monitoring = get_monitoring(soup)
                    print(type(monitoring))
                        #print(type(monitoring[0]))
                        # print(monitoring)
                    for element in monitoring:
                        print(element)
                        player = Player.objects.get_or_create(name=element[0].text, url= MAIN_URL + element[0]['href'])[0]
                        print(player)
                        if element[1] == 'w':
                            correct = False
                        else:
                            correct = True
                            # print(player, element[2], correct)
                        if Code.objects.filter(code_text=element[2], correct=correct, player=player, game=game).exists():
                            print('Такой код этот игрок уже вбивал')
                        else:
                            c = Code.objects.create(code_text=element[2], correct=correct)
                            c.player.add(player)
                            c.game.add(game)
                            c.save()
                except:
                    print('Проблемы с мониторингом:(')

            for author in authors:
                player = Player.objects.get(name=author.text)
                Author.objects.get_or_create(player=player, game=game)



        except:
            pass


        print('=========================================================================\n\n')
        sleep(randint(5,15))


"""
with open('game.html', 'w') as i:
    i.write(rr.text)"""

"""
def get_general_game_information(soup):
    game_title = soup.find(id="lnkGameTitle")
"""



