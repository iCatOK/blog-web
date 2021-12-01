from pywebio.output import put_buttons, put_markdown, put_row, style
from pywebio.session import go_app
from cookie_io import get_current_user_id, init_js_cookie_io, remove_user_info
from sql import get_user_by_id
from utils import put_empty_row
from styles import *


# глобальные переменные страницы
page_globals = {
    'current_user': None
}


# стереть глобальные переменные страницы
def clear_page_globals():
    global page_globals
    page_globals = {
        'current_user': None
    }


# получение пользователя из id в куки
def set_user_from_cookie():
    global page_globals
    id = get_current_user_id()
    if(id != None):
        user = get_user_by_id(id)
        if(user != None):
            page_globals['current_user'] = user


# выход из учетной записи
def logout():
    remove_user_info()
    clear_page_globals()
    go_app('auth_page', new_window=False)


# результаты
def credits():
    ...
    #go_app('results_page', new_window=False)

# основной код страницы выбора теста
def home_page():
    init_js_cookie_io()
    set_user_from_cookie()

    print(page_globals)

    if(page_globals['current_user'] == None):
        go_app('auth_page', new_window=False)

    print()

    put_row(
        [put_markdown('# Блог'), 
            None, style(put_buttons(['Об авторе', 'Выйти'], [credits, logout]), 'align-self: center')
        ], size='60% 10px 40%'
    )
    put_empty_row()
    

    
