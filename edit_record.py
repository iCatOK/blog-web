# основной код страницы выбора теста
from pywebio.output import put_buttons, put_markdown, put_text
from pywebio.pin import pin, put_input, put_textarea
from pywebio.session import go_app
from cookie_io import get_current_record_id, get_current_user_id, init_js_cookie_io
from sql import get_record_by_id, get_user_by_id, update_diary_record


# глобальные переменные страницы
page_globals = {
    'current_user': None,
    'current_record': None
}


# обновить текст записи
def update_record(text: str):
    print(text)
    update_diary_record(page_globals['current_record'].id, text)
    go_app('home_page', new_window=False)


# получение пользователя из id в куки
def set_user_from_cookie():
    global page_globals
    id = get_current_user_id()
    if(id != None):
        user = get_user_by_id(id)
        if(user != None):
            page_globals['current_user'] = user


def edit_record_page():
    init_js_cookie_io()
    set_user_from_cookie()

    page_globals['current_record'] = get_record_by_id(get_current_record_id())

    if(page_globals['current_user'] == None):
        go_app('auth_page', new_window=False)
    
    if(page_globals['current_record'] == None):
        go_app('home_page', new_window=False)
    
    put_markdown("# 🖊️ Редактирование")
    put_textarea('new_text', value=page_globals['current_record'].record_text)
    put_buttons(['Готово'], [lambda: update_record(pin.new_text)])

    
