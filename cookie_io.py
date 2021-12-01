from pywebio.session import eval_js, run_js


# литералы для сохранения переменных куки
current_user_id = 'current_user_id'
current_record_id = 'current_record_id'

# список литералов
literals = [
    current_user_id,
    current_record_id
]


# инициализация js кода для взаимодействия с куки
def init_js_cookie_io():
    run_js("""
        window.setCookie = function(name,value,days) {
            var expires = "";
            if (days) {
                var date = new Date();
                date.setTime(date.getTime() + (days*24*60*60*1000));
                expires = "; expires=" + date.toUTCString();
            }
            document.cookie = name + "=" + (value || "") + expires + "; path=/";
        }
        
        window.getCookie = function(name) {
            var nameEQ = name + "=";
            var ca = document.cookie.split(';');
            for(var i=0;i < ca.length;i++) {
                var c = ca[i];
                while (c.charAt(0)==' ') c = c.substring(1,c.length);
                if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
            }
            return null;
        }

        window.deleteCookie = function(name) {
            document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        }
        """
    )


# создание переменной
def set_cookie(key, value, days=30):
    run_js("setCookie(key, value, days)", key=key, value=value, days=days)


# получение переменной
def get_cookie(key):
    return eval_js("getCookie(key)", key=key)


# удаление куки
def remove_cookie(key):
    run_js('deleteCookie(key)', key=key)


# сохранить id записи в куки
def save_current_record_id(id: int):
    set_cookie(current_record_id, f'{id}')


# получить id записи из куки
def get_current_record_id():
    id = get_cookie(current_record_id)
    return None if id == None or id == '' else int(id)


# удалить информацию о записи
def remove_record_info():
    remove_cookie(current_record_id)


# сохранить id пользователя в куки
def save_current_user_id(id: int):
    set_cookie(current_user_id, f'{id}')


# получить id пользователя из куки
def get_current_user_id():
    id = get_cookie(current_user_id)
    return None if id == None or id == '' else int(id)


# удалить информацию о пользователе
def remove_user_info():
    remove_cookie(current_user_id)


# удалить все куки
def remove_all_cookies():
    for literal in literals:
        remove_cookie(literal)

