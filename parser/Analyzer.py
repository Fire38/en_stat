import requests
import threading
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from get_functions import *

from backend.models import Game, Team, Player, Personal_statistic, Rating, Code, Author



class Analyzer(threading.Thread):
    def __init__(self, queue, session, cookies, headers):
        """Инициализация потока"""
        threading.Thread.__init__(self)
        self.queue = queue
        self.session = session
        self.cookies = cookies
        self.headers = headers

    def run(self):
        """Запуск потока"""
        while True:
            # Получаем url из очереди
            url = self.queue.get()
            # Анализируем игру
            self.analyze(url)
            # Отправляем сигнал о том, что задача завершена
            self.queue.task_done()

    def analyze(self, url):

        print(url)
        res = self.session.get(url, headers=self.headers, cookies=self.cookies)
        soup = BeautifulSoup(res.text, 'html.parser')
        print(url)
        game_title, game_diff, quality_index, game_type, forum_resonance, date, authors = get_general_game_information(
            soup)

        game = Game.objects.get_or_create(name=game_title.text,
                                          url=url,
                                          diff_game=game_diff.text,
                                          quality_index=quality_index,
                                          game_type=game_type,
                                          forum_resonance=forum_resonance,
                                          finish_date=date)[0]
        winner = get_winner(soup, game_type)
        game.winner = winner
        game.save()

        # Если у игры не стоит флаг, что все данные собраны
        if game.done:
            pass
        else:
            if game_type == 'Командная':
                # Получаем команды которые играли
                teams = get_games_teams(self.session, self.cookies, self.headers, soup, game_type)
                print('Количество команд ', len(teams))
                if teams:
                    game.team_count = len(teams)
                    for team in teams:
                        t = Team.objects.get_or_create(name=team.text, url=MAIN_URL+team['href'])[0]
                        game.team.add(t)
                else:
                    game.team_count = 0
                game.save()

                try:
                    # Выясняем кто за кого играл
                    playing_teams = get_teams_players(self.session, self.cookies, self.headers, soup)
                    for team_name, player_list in playing_teams.items():
                        team = Team.objects.get(name=team_name)
                        for player in player_list:
                            player = Player.objects.get_or_create(name=player.text, url=MAIN_URL + player['href'])[0]
                            Personal_statistic.objects.get_or_create(player=player, game=game, team=team)
                        # Если команда - победитель, начисляем каждому игроку +1 победу
                        if team_name == game.winner:
                            for player in playing_teams[team_name]:
                                player = Player.objects.get(name=player.text)
                                player.victory_count += 1
                                player.save()
                except:
                    pass

                # Получаем оценки игроков за игру
                rate_dict = get_player_rate(self.session, self.cookies, self.headers, soup)
                for player_name, rate in rate_dict.items():
                    player = Player.objects.get(name=player_name)
                    Rating.objects.get_or_create(player=player, game=game, rate=rate)

                # Если мониторинг открыт
                # print(self.session.cookies)
                monitoring = get_monitoring(self.session, self.cookies, self.headers, soup)
                """
                except:
                    with open('monitoring.txt', 'a') as f:
                        f.write(game.name + '\n')
                    headers = {'User-Agent': UserAgent(use_cache_server=True).random}

                    session = requests.Session()
                    res = session.get(LOGIN_URL, headers=headers)
                    # print(session.cookies)
                    data = {**LOGIN_DATA, **res.cookies.get_dict()}
                    res = session.post(LOGIN_URL, params=data, headers=headers, allow_redirects=False)
                    res = session.get(MAIN_URL, headers=headers)
                    cookies = session.cookies
                    monitoring = get_monitoring(session, cookies, headers, soup)"""

                for element in monitoring:
                    print(element)
                    player = Player.objects.get_or_create(name=element[0].text, url=MAIN_URL + element[0]['href'])[0]
                    print(player)
                    if element[1] == 'w':
                        correct = False
                    else:
                        correct = True
                        # print(player, element[2], correct)
                    if Code.objects.filter(code_text=element[2], correct=correct, player=player,
                                           game=game).exists():
                        print('Такой код этот игрок уже вбивал')
                    else:
                        c = Code.objects.create(code_text=element[2], correct=correct)
                        c.player.add(player)
                        c.game.add(game)
                        c.save()

            for author in authors:
                player = Player.objects.get(name=author.text)
                Author.objects.get_or_create(player=player, game=game)
            game.done = True
            game.save()



        print('\n====================================================\n')
