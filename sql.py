import sqlite3
from typing import Any
from pywebio.session import go_app
from classes.diary_record import DiaryRecord
from classes.user import User
from sqlite3 import Error
from messages import set_message


db = sqlite3.connect('db_blog.db', check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES)


# клиент бд
sql = db.cursor()


# запросы к бд
get_user_by_username_query = "select * from user where username = '%s'"
get_user_by_id_query = "select * from user where id = %s"
register_user_query = "insert into user (name, username, password) values ('%s', '%s', '%s')"
get_diary_records_by_id_query = "select * from diary_records where user_id = %s"
add_diary_record_query = "insert into diary_records (user_id, record_text) values (%s, '%s')"
update_diary_record_text_query = "update diary_records set record_text = '%s' where id = %s"
update_diary_record_date_query = "update diary_records set record_date = current_timestamp where id = %s"
delete_diary_record_query = "delete from diary_records where id = %s"
get_record_by_id_query = "select * from diary_records where id = %s"

# логгер sql
def log(message):
    print(f'[SQL] {message}...')


# обёртка для функций sql - проверка на ошибки внутри sql
def sql_error_check(query_function) -> Any:
    def wrapper(*args, **kwargs):
        try:
            return query_function(*args, **kwargs)
        except Error as e:
            if(db): db.rollback()
            return f"Ошибка БД! {' '.join(e.args)}"
        except Exception as e:
            if(db): db.rollback()
            return f"Ошибка! {' '.join(e.args)}"
    return wrapper


# проверка пользователя
@sql_error_check
def validate_credentials(username: str, password: str) -> Any:
    sql.execute(get_user_by_username_query % username)
    user_tuple: tuple = sql.fetchone()
    if(user_tuple is None):
        return 'Пользователь не зарегистрован. Перейдите на страницу регистрации'
    else:
        user = User(user_tuple)
        if(user.password == password):
            return user
        else:
            return 'Логин и пароль не совпадают!'


# получение пользователя по id
def get_user_by_id(id: int):
    sql.execute(get_user_by_id_query % id)
    user_tuple: tuple = sql.fetchone()
    if(user_tuple is None):
        return None
    else:
        user = User(user_tuple)
        return user


# регистрация пользователя
@sql_error_check
def register_user(name: str, username: str, password: str) -> Any:
    sql.execute(get_user_by_username_query % username)
    user_tuple: tuple = sql.fetchone()
    if(user_tuple is not None):
        return 'Пользователь уже зарегистрирован. Выберете другой логин!'
    
    sql.execute(register_user_query % (name, username, password))
    db.commit()
    set_message('Вы успешно зарегистрировались!')
    go_app('auth_page', new_window=False)


# получение дневника пользователя
@sql_error_check
def get_diary_records_by_id(id: int) -> list:
    sql.execute(get_diary_records_by_id_query % id)
    records = [DiaryRecord(record_tuple) for record_tuple in sql.fetchall()]
    return records


# получение записи по id
def get_record_by_id(id: int):
    log('Получение записи по id')
    sql.execute(get_record_by_id_query % id)
    record_tuple: tuple = sql.fetchone()
    if(record_tuple is None):
        return None
    else:
        record = DiaryRecord(record_tuple)
        return record


# удаление записи дневника
@sql_error_check
def delete_diary_record(record_id: int):
    sql.execute(delete_diary_record_query % record_id)
    db.commit()


# обновление записи дневника
@sql_error_check
def update_diary_record(record_id: int, record_text: str):
    print(record_id, record_text)
    sql.execute(update_diary_record_date_query % (record_id))
    db.commit()
    sql.execute(update_diary_record_text_query % (record_text, record_id))
    db.commit()


# добавление записи дневника
@sql_error_check
def add_diary_record(user_id: int, record_text: str):
    sql.execute(add_diary_record_query % (user_id, record_text))
    db.commit()