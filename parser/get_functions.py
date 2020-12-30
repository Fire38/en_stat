import re
import pprint
import requests
import datetime
from time import sleep
from random import randint
from bs4 import BeautifulSoup
from config import GAME_LIST_URL, MAIN_URL, PAGE_COUNT, LOGIN_URL, LOGIN_DATA
from backend.models import Player


def get_games_url_list(session, cookies, headers):
    """ Список url всех игр """
    game_list = []
    for i in range(1, PAGE_COUNT+1):
        print('Сбор url с страницы {}'.format(i))
        res = session.get(GAME_LIST_URL + str(i), cookies=cookies, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        games = soup.find_all(id='lnkGameTitle')
        for game in games:
            game_list.append(MAIN_URL + game['href'])
    return game_list


def get_general_game_information(soup):
    """ Собирает общую информацию об игре """
    game_title = soup.find(id='lnkGameTitle')
    print('Название игры: ', game_title.text)

    # re потому что id авторов отличаются
    authors = soup.find_all(id=re.compile("GameDetail_AuthorsRepeater_ct"))
    for author in authors:
        Player.objects.get_or_create(name=author.text, url=MAIN_URL + author['href'])
        print("Автор: " + author.text)

    game_diff = soup.find(id='GameDetail_lnkGameComplexity')
    print('Коэффициент сложности игры: ', game_diff.text)

    try:
        quality_index = soup.find(id='GameDetail_lnkGameQuality').text
        # Если игра признана несостоявшейся или еще по какой-то причине индекса нет
        if quality_index == '-':
            quality_index = 0.0
        game_type = 'Командная'
    except:
        quality_index = 0.0
        game_type = 'Одиночная игра'
    print('Индекс качества игры: ', quality_index)

    """
    # Цепляемся за статистику, а в родительском элементе количество команд
    try:
        team_count = soup.find(id='GameDetail_lnkGameStat').parent.text
        if 'teams' in team_count:
            team_count = team_count.split(' ')[0].strip()
            team_count = team_count.replace(u'\xa0', u' ').split(' ')[0]
            print("Количество команд: ", team_count)
        else:
            game_type = "Одиночка на движке схватки"
            team_count = 0
            print("Одиночка на движке схватки")
    except:
        team_count = 0
        print('Одиночная игра')
    """

    forum_resonance = soup.find(id='GameDetail_lnkGuestBook').text.split(' ')[0]
    print('Сообщений на форуме: ', forum_resonance)

    finish_date = soup.find(id='top10Winners_SingleRepeater_ctl01_TdWinDateTime')

    # Костыль с датами
    try:
        date = datetime.datetime.strptime(finish_date.text.split(' ')[0].strip(), '%m/%d/%Y') - datetime.timedelta(days=1)
        print(date)
    except:
        date = datetime.date(year=1999, month=1, day=1)
    return game_title, game_diff, quality_index, game_type, forum_resonance, date, authors


def get_winner(soup, game_type):
    """ Возвращает победителя. Если игра некомандная, то не ищем """
    if game_type == 'Командная':
        winner = soup.find(id='top10Winners_SingleRepeater_ctl01_lnkWinnerInfo')
        print("Победитель: ", winner.text)
        return winner.text
    elif game_type == 'Одиночка на движке схватки':
        winner = "Не команда"
    else:
        # если одиночка
        winner = soup.find(id="wetWarsTop10Winners_SingleRepeater_ctl01_lnkWinnerInfo")
        print("Победитель:", winner.text)
    return winner.text


def get_games_teams(session, cookies, headers, soup, game_type):
    """ Возвращает команды принимающие участие в конкретной игре """
    print('Ищем учавствующие команды \n')
    if game_type == 'Командная':
        total_teams_link = soup.find(id="lnkTopFull")
        team_list = []
        if total_teams_link is not None:
            list_url = total_teams_link['href']
            res = session.get(MAIN_URL + list_url, headers=headers, cookies=cookies)

            soup = BeautifulSoup(res.text, 'html.parser')
            teams = soup.find_all(id=re.compile("top10Winners_SingleRepeater_ctl[0-9]{1,3}_lnkWinnerInfo"))
            for team in teams:
                team_list.append(team)
        else:
            teams = soup.find_all(id=re.compile("top10Winners_SingleRepeater_ctl[0-9]{1,3}_lnkWinnerInfo"))
            for team in teams:
                team_list.append(team)
        return team_list
    return None


def get_teams_players(session, cookies, headers, soup):
    """ Состав команды на конкретную игру """
    print("Собираем информацию о составах команд\n")
    full_team_url = soup.find(id='lnkWinnerMembersEdit')
    res = session.get(MAIN_URL + full_team_url['href'], headers=headers, cookies=cookies)
    page_block = res.text.split('Team:')
    team_dict = {}
    for page in page_block:
        soup = BeautifulSoup(page, 'html.parser')
        players = soup.find_all(id=re.compile("WinnersRepeater_ctl"))
        team_name = soup.find('span', class_='gold bold')
        # print("Название команды", team_name)
        team = []
        for player in players:
            team.append(player)
        try:
            team_dict[team_name.text] = team
        except:
            pass
    return team_dict


def get_player_rate(session, cookies, headers, soup):
    """ Определяет какую оценку поставил игрок в конкретной игре """
    try:
        full_teams_list = soup.find(id='lnkTopFull')
        res = session.get(MAIN_URL + full_teams_list['href'], cookies=cookies, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
    except:
        pass

    rate_links = soup.find_all(id=re.compile('_TeamRateLink'))
    player_rate_dict = {}
    print("\nЗаписываем оценки игроков\n")
    for rate_link in rate_links:
        # страхуемся что никто в команде не поставил оценку
        try:
            res = session.get(MAIN_URL + rate_link['href'], cookies=cookies, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            player_lines = soup.find_all(class_='toWinnerItem')
            for line in player_lines:
                player = line.find(id=re.compile('_lnkUserInfo'))
                rate = line.find(class_=re.compile('topWinners pink'))
                player_rate_dict[player.text] = rate.text
        except:
            print("Без оценок")
    pprint.pprint(player_rate_dict)
    return player_rate_dict


def get_monitoring(session, cookies, headers, soup):
    """  Анализируем кто какие коды вбивал """
    """
    session = requests.Session()
    res = session.get(LOGIN_URL, headers=headers)

    data = {**LOGIN_DATA, **res.cookies.get_dict()}
    res = session.post(LOGIN_URL, params=data, headers=headers, allow_redirects=False)"""

    # print(session.cookies)
    monitoring_href = soup.find(id='GameDetail_lnkMonitoring')
    # print(MAIN_URL + monitoring_href['href'])
    res = session.get(MAIN_URL + monitoring_href['href'], cookies=cookies, headers=headers)
    page = BeautifulSoup(res.text, 'html.parser')

    paginator = page.find_all('a', href=re.compile('Administration/Games/ActionMonitor.aspx\?gid='))
    last_page = paginator[len(paginator)-1].text

    i = 1
    code_list = []

    while i <= int(last_page):
        print(MAIN_URL + monitoring_href['href'] + '&page=' + str(i))
        res = session.get(MAIN_URL + monitoring_href['href'] + '&page=' + str(i), cookies=cookies, headers=headers)
        player_block = res.text.split('padL5')
        for block in player_block:
            soup = BeautifulSoup(block, 'html.parser')
            try:
                sublist = []
                player = soup.find(id=re.compile('lnkUserInfo'))
                code_type = soup.find(id=re.compile('_lblCorrectValue'))
                code_text = soup.find_all('span', class_='nonLatinChar')
                if code_text == []:
                    code_text = code_type.parent.findNext('td').text
                    parent = code_text
                else:
                    parent = code_text[0].parent.text
                sublist.append(player)
                sublist.append(code_type.text)
                sublist.append(parent)
                print("Строка мониторинга: ", sublist)
                code_list.append(sublist)
            except:
                pass
        print('====================================================\n')
        i += 1
        sleep(randint(5, 7))

    return code_list
