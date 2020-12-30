import re
import os
import sys
import pprint
import django
import requests
import datetime
import threading
from queue import Queue
from time import sleep
from random import randint
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


# магия импортов
sys.path.append('/home/roman/env/en_stat1/en_statistic/')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "en_statistic.settings")
django.setup()
from backend.models import Game, Team, Player, Personal_statistic, Rating, Code, Author

from config import *
from get_functions import get_games_url_list
from Analyzer import Analyzer


headers = {'User-Agent': UserAgent(use_cache_server=True).random}

session = requests.Session()
res = session.get(LOGIN_URL, headers=headers)
# print(session.cookies)
data = {**LOGIN_DATA, **res.cookies.get_dict()}
res = session.post(LOGIN_URL, params=data, headers=headers, allow_redirects=False)
res = session.get(MAIN_URL, headers=headers)
cookies = session.cookies


if __name__ == "__main__":

    game_urls = get_games_url_list(session, cookies, headers)
    # Создаем экземпляр очереди
    queue = Queue()

    for i in range(THREAD_COUNT):
        # передаем очередь N количеству потоков
        t = Analyzer(queue, session, cookies, headers)
        # делаем демонизированными чтобы сами завершались
        t.setDaemon(True)
        t.start()

    # Загружаем url в очередь

    for url in game_urls:
        queue.put(url)
    # queue.put('http://vbratske.en.cx/GameDetails.aspx?gid=68747')
    # Говорим чтобы очередь подождала пока потоки выполнят свои процессы
    queue.join()



