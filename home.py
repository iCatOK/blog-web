from pywebio.output import put_button, put_buttons, put_column, put_markdown, put_row, put_text, style, use_scope
from pywebio.session import go_app
from classes.diary_record import DiaryRecord
from cookie_io import get_current_user_id, init_js_cookie_io, remove_user_info, save_current_record_id
from sql import delete_diary_record, get_diary_records_by_id, get_user_by_id
from utils import centered_container, put_empty_row
from styles import *
from classes.diary_record import current_record
import classes.diary_record as diary

# глобальные переменные страницы
page_globals = {
    'current_user': None
}


test_cell_container_style = '''
    align-items: center;
    align-self: center;
    display: flex;
    flex-direction: column;
    margin: 20px;
    background-color: #efefef;
    border-radius: 10px;
    padding: 10px;
    width: 800px;
'''


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


# удаление записи
def delete_record(record_id: int):
    delete_diary_record(record_id)
    centered_container(put_record_list())


# редактирование записи
def edit_record(record: DiaryRecord):
    save_current_record_id(record.id)
    go_app('edit_record_page', new_window=False)


def add_record():
    go_app('add_record_page', new_window=False)


# результаты
def credits():
    ...
    #go_app('results_page', new_window=False)


# стиль контейнера
def record_container(output):
    return style(output, test_cell_container_style)


# код для описания записи
def record_md(record: DiaryRecord):
    markdown = ''
    date = record.record_date.strftime('%m/%d/%Y %H:%M:%S')
    markdown += f'### 📆 Дата: {date}\n'
    markdown += f"📖 {record.record_text}"
    return put_markdown(markdown)


# добавление одной записи
def put_record(record: DiaryRecord):
    return record_container(
        put_column([
            record_md(record),
            put_buttons(['Редактировать', 'Удалить'], [lambda: edit_record(record), lambda: delete_record(record.id)])
        ])
    )


# формирование контейнера со списком тестов
@use_scope('diary_records', clear=True)
def put_record_list():
    diary_list = []
    diary_set = get_diary_records_by_id(page_globals['current_user'].id)

    if(len(diary_set) == 0):
        return put_text('Дневник пуст! Добавьте запись!')

    for record in diary_set:
        diary_list.append(put_record(record))
    return put_column(diary_list)


# основной код страницы выбора теста
def home_page():
    init_js_cookie_io()
    set_user_from_cookie()

    if(page_globals['current_user'] == None):
        go_app('auth_page', new_window=False)

    put_row(
        [put_markdown('# Дневник'), 
            None, style(put_buttons(['Добавить запись', 'Выйти'], [add_record, logout]), 'align-self: center')
        ], size='60% 10px 40%'
    )

    put_empty_row()

    centered_container(put_record_list())

    
    

    
