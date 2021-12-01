from pywebio.platform import start_server
from pywebio.session import go_app
from add_record import add_record_page

from auth import auth_page
from home import home_page
from edit_record import edit_record_page
from register import register_page
from cookie_io import init_js_cookie_io, remove_all_cookies


# главная страница сайта - редирект на страницу авторизации
def index():
    init_js_cookie_io()
    go_app('auth_page', new_window=False)


# основные модули сайта
main_router = [
    index,
    register_page,
    auth_page,
    home_page,
    edit_record_page,
    add_record_page
]


# запуск сайта
start_server(main_router, port=8080, debug=True)