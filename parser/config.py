DOMAIN = "vbratske"

LOGIN = 'f1re'

PASSWORD = 'Zte261192'

# Количество потоков
THREAD_COUNT = 1

# Количество страниц статистики
PAGE_COUNT = 8

LOGIN_DATA = {
    'Login': LOGIN,
    'Password': PASSWORD,
    'socailAssign': '0',
    'EnButton1': 'Sign In',
    'ddlNetwork': '1',
    'mobile': '0'
}

MAIN_URL = 'http://{}.en.cx'.format(DOMAIN)

LOGIN_URL = "http://{}.en.cx/Login.aspx".format(DOMAIN)

# Страницы с прошедшими играми
GAME_LIST_URL = 'http://{}.en.cx/Games.aspx?page='.format(DOMAIN)

