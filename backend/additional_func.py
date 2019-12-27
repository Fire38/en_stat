from .models import *
from django.db.models import Q


def get_count_code():
    """ Возвращает количество игр в которых использовался тот или иной правильный код """

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


def dict_sort(d):
    """ Сортирует список правильных кодов из get_count_code """
    list_d = list(d.items())

    list_d.sort(key=lambda i: i[1])
    return list_d