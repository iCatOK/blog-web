# основной код страницы выбора теста
from pywebio.output import put_buttons, put_markdown
from pywebio.pin import pin, put_textarea
from pywebio.session import go_app
from cookie_io import get_current_user_id, init_js_cookie_io
from sql import add_diary_record, get_user_by_id


# глобальные переменные страницы
page_globals = {
    'current_user': None,
}


# обновить текст записи
def add_record(text: str):
    print(text)
    add_diary_record(page_globals['current_user'].id, text)
    go_app('home_page', new_window=False)


# получение пользователя из id в куки
def set_user_from_cookie():
    global page_globals
    id = get_current_user_id()
    if(id != None):
        user = get_user_by_id(id)
        if(user != None):
            page_globals['current_user'] = user


def add_record_page():
    init_js_cookie_io()
    set_user_from_cookie()

    if(page_globals['current_user'] == None):
        go_app('auth_page', new_window=False)
    
    put_markdown("# 📝 Добавление")
    put_textarea('new_text', placeholder="Напишите, что случилось с вами сегодня")
    put_buttons(['Добавить'], [lambda: add_record(pin.new_text)])

    
