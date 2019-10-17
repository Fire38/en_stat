import re
import os
import django
import requests
import datetime
from time import sleep
from random import randint
from bs4 import BeautifulSoup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "en_statistic.settings")
django.setup()

from backend.models import Game, Team, Player

LOGIN_URL = "http://vbratske.en.cx/Login.aspx"
LOGIN_DATA = {'Login': 'f1re', 'Password': 'Zte261192'}

MAIN_URL = "http://vbratske.en.cx"
# получаем токен, ид сессии
session = requests.Session()
res = session.get(LOGIN_URL)

data = {**LOGIN_DATA, **res.cookies.get_dict()}

res = session.post(LOGIN_URL, params=data)
print(res.status_code)


def get_domain_teams_list():
    """Все команды домена"""
    for i in range(1,10):
        url = "http://vbratske.en.cx/Teams/TeamList.aspx?page=" + str(i)
        rr = session.get(url)
        soup = BeautifulSoup(rr.text, 'html.parser')
        teams = soup.find_all(id=re.compile("_lnkTeamInfo"))
        for team in teams:
            print(team.text)
            Team.objects.get_or_create(name=team.text, url=MAIN_URL+team['href'])


def get_games_teams(soup, game_type):
    """Команды принимающие участие в конкретной игре"""
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


def get_teams_players(soup):
    """Состав команды на конкретную игру"""
    full_team_url = soup.find(id='lnkWinnerMembersEdit')

    res = session.get(MAIN_URL + full_team_url['href'])
    page_block = res.text.split('Team:')
    for page in page_block:
        # print("БЛОК-------------------", page)
        soup = BeautifulSoup(page, 'html.parser')
        players = soup.find_all(id=re.compile("WinnersRepeater_ctl"))
        team_name = soup.find('span', class_='gold bold')
        print("Название команды", team_name)
        team = []
        for player in players:
            team.append(player.text)
        print("Игроки команды", team)
        #print("------------------------\n")


#get_domain_teams_list()


def get_general_game_information(soup):
    game_title = soup.find(id='lnkGameTitle')
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
        date = datetime.date(year=2020, month=1, day=1)

    return game_title, url, game_diff, quality_index, team_count, game_type, forum_resonance, date


GAME_LIST_URL = "http://vbratske.en.cx/Games.aspx?page="
for i in range(1,7):
    rr = session.get(GAME_LIST_URL + str(i))
    soup = BeautifulSoup(rr.text, 'html.parser')
    game_list = []
    games = soup.find_all(id='lnkGameTitle')
    for game in games:
        game_list.append(game['href'])

    for game_href in game_list:
        url = 'http://vbratske.en.cx' + game_href
        print(url)
        res = session.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        game_title, url, game_diff, quality_index, team_count, game_type, forum_resonance, date = get_general_game_information(soup)

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
            # получаем команды для добавления в таблицу игр
            teams = get_games_teams(soup, game_type)
            for team in teams:
                t = Team.objects.get(name=team.text)
                game.team.add(t)
                game.save()
            # TODO какой игрок в какой команде был на какой игре
            get_teams_players(soup)
            print('=========================================================================\n\n')
            sleep(randint(0,3))


"""
with open('game.html', 'w') as i:
    i.write(rr.text)"""

"""
def get_general_game_information(soup):
    game_title = soup.find(id="lnkGameTitle")
"""



