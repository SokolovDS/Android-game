#-*- coding: utf-8 -*-


#Сервер


#Библиотеки для работы сервера
from flask import Flask, request, json, session, g, redirect, url_for, abort, render_template, flash

#Сторонние библиотеки
from random import randrange
import sqlite3
import os


#Файлы дополнительных скриптов


#Переменные
DATABASE = '/tmp/game_db.db'



app = Flask(__name__)  #Основной класс приложения


app.config.from_object(__name__) #Класс конфигов


app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'game_db.db') ) ) #Подгрузка конфигов


app.config.from_envvar('MAIN_FLASK_SETTINGS', silent = True) #Инициализация конфигов



def connect_db(): #Установка связи с базой данных

    bd_connect = sqlite3.connect(app.config['DATABASE'])
    bd_connect.row_factory = sqlite3.Row
    return bd_connect



def init_db():  #Инициализация базы данных

    with app.app_context():
        db = get_db()
        with app.open_resource('db_plane.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()



def get_db(): #Подключение к бд если его ещё не было

    if not hasattr(g, 'game_db.db'):
        g.game_db = connect_db()
    return g.game_db



def email_search(email): #Поиск почты в базе данных

    ret_var = ''
    local_spisok = []
    email = str(email)

    if '@' in email:

        db = get_db()
        cur = db.execute('select email, user_id from users order by id desc')
        all_users = cur.fetchall()

        for var in all_users:

            if email in var:
                ret_var = var[1]
                local_spisok.clear()
                break

            else:
                local_spisok.append(var[1])


        else:

            us_id = randrange(10000, 99999)
            us_id = str(us_id)

            while us_id in local_spisok:

                us_id = randrange(10000, 99999)
                us_id = str(us_id)

            ret_var = us_id

            db.execute('insert into users (email, user_id) values ( "{value_1}", "{value_2}" )'.format(value_1 = email, value_2 = us_id) )
            db.commit()


    else:
        ret_var = 'Error'

    return ret_var



def id_search(idd): #Поиск id базе данных

    idd = str(idd)

    if idd.isdigit() == True:

        db = get_db()
        cur = db.execute('select email, user_id from users order by id desc')
        all_users = cur.fetchall()

        for var in all_users:

            if idd in var:
                ret_var = True
                break

        else:
            ret_var = False


    else:
        ret_var = 'Error'

    return ret_var


def spisok_list(local_spisok):

    ret_var = ''

    if local_spisok != []:

        ret_var = '|'.join(local_spisok)



    return ret_var


def role_gen(ses_id):   #1 - инквизитор; 0 - еретик | инквизиторв в сессии - 2; еретиков - 3

    role_spisok = []
    ret_var = ''

    local_spisok = ses_dct[ses_id]

    if local_spisok != []:

        for var in local_spisok:

            if role_dct != {}:
                role_spisok.append(role_dct.get(var))

            elif role_dct == {}:
                ret_var = '1'
                break

        else:

            #er = role_spisok.count('0')
            ink = role_spisok.count('1')

            if ink < 2:
                ret_var = '1'

            elif ink >= 2:
                ret_var = '0'

            else:
                ret_var = 'error'

    elif local_spisok == []:
        ret_var = '1'

    else:
        ret_var = 'error'

    return ret_var


def ses_id_gen():

    local_spisok = []
    ret_var = ''

    if ses_dct != {}:

        for var in ses_dct:
            local_spisok.append(var)

        ses_id = randrange(100, 999)
        ses_id = str(ses_id)

        while ses_id in local_spisok:

            ses_id = randrange(100, 999)
            ses_id = str(ses_id)

        ret_var = ses_id

    elif ses_dct == {}:

        ses_id = randrange(100, 999)
        ses_id = str(ses_id)
        ret_var = ses_id

    else:
        ret_var = 'Error'

    return ret_var
#------------------------------------------------------


global data_dct; data_dct = {}
global ses_dct; ses_dct = {}
global cur_users; cur_users = []
global cur_ses; cur_ses = []

global role_dct; role_dct = {} #1 - инквизитор; 0 - еретик
global stat_dct; stat_dct = {}

# -----------------------------------------------------

@app.teardown_appcontext

def close_db(error): #Разрыв соеденения с базой данной

    if hasattr(g, 'game_db'):
        g.game_db.close()



@app.route('/show_users') #Показ базы данных по ссылке

def show_users():

    local_dct = {}

    db = get_db()
    cur = db.execute('select email, user_id from users order by id desc')
    users = cur.fetchall()

    for var in users:
        local_dct[var[1]] = var[0]


    return json.dumps(local_dct)



@app.route('/send_email', methods=['GET'])  #Регистрация по email

def send_email():

    get_email = request.args['email']

    ret_var = ''

    value = email_search(get_email)

    if value.isdigit() == True:
        ret_var = value
        cur_users.append(str(ret_var))

    else:
        ret_var = 'Error'


    return json.dumps(ret_var)


@app.route('/get_cur_users', methods = ['GET']) #Кол - во текущих игроков в сесси

def get_cur_users():

    get_id = request.args['idd']

    ret_var = ''

    value = id_search(get_id)

    if value == True:
        ret_var = len(cur_users)
        ret_var = str(ret_var)

    else:
        ret_var = 'Error'

    return json.dumps(ret_var)


@app.route('/get_cur_ses', methods = ['GET']) #Список всех созданных сессий

def get_cur_ses():

    get_id = request.args['idd']

    ret_var = ''
    local_spisok = []

    value = id_search(get_id)

    if value == True:

        if cur_ses != []:

            local_spisok = cur_ses.copy()

            ret_var = spisok_list(local_spisok)

        else:
            ret_var = '0'

    else:
        ret_var = 'Error'

    return json.dumps(ret_var)


@app.route('/create_ses', methods = ['GET']) #Создание сессии

def create_ses():

    get_id = request.args['idd']
    get_id = str(get_id)


    ret_var = ''
    local_spisok = []

    value = id_search(get_id)

    if value == True:

        for var in ses_dct:
            local_spisok.extend(ses_dct.get(var))


        if get_id not in local_spisok:


            s_id = ses_id_gen()

            cur_ses.append(s_id)

            ses_dct[s_id] = [get_id]
            ret_var = 'True'

            var_role = role_gen(s_id)
            role_dct[get_id] = var_role
            stat_dct[get_id] = False
            data_dct[get_id] = ''

        else:
            ret_var = 'False'

    else:
        ret_var = 'Error'

    return json.dumps(ses_dct) #доделать


@app.route('/join_ses', methods = ['GET']) #Подключение к сессии

def join_ses():

    get_id = request.args['idd']
    ses_id = request.args['ses']

    get_id = str(get_id)
    ses_id = str(ses_id)

    ret_var = ''
    local_spisok = []
    second_spisok = []
    all_spisok = []


    value = id_search(get_id)

    if value == True:

        local_spisok = ses_dct.get(ses_id)

        if len(local_spisok) >= 5 or get_id in local_spisok:

            ret_var = 'False'

        elif len(local_spisok) < 5:

            if ses_dct != {}:

                for var in ses_dct:
                   all_spisok.extend(ses_dct.get(var))


            if get_id not in local_spisok and get_id not in all_spisok or all_spisok == []:

                ret_var = 'True'
                local_spisok.append(str(get_id))
                ses_dct[str(ses_id)] = local_spisok

                var_role = role_gen(ses_id)

                role_dct[get_id] = var_role
                stat_dct[get_id] = False
                data_dct[get_id] = ''

        else:
            ret_var = 'Error'

    else:
        ret_var = 'Error'

    return json.dumps(ses_dct) #Доделать


@app.route('/role', methods = ['GET'])
def role():

    return json.dumps(str(role_dct) + str(stat_dct) + 'sessions' + str(ses_dct) + str(data_dct))


@app.route('/get_user_in_ses', methods = ['GET'])

def get_user_in_ses():

    get_id = request.args['idd']
    ses_id = request.args['ses']

    ses_id = str(ses_id)
    get_id = str(get_id)

    local_spisok = []
    user_spisok = []
    ret_var = ''

    value = id_search(get_id)

    if value == True:

        local_spisok = ses_dct.get(ses_id)

        if get_id in local_spisok:
            local_spisok.remove(get_id)

        for var in local_spisok:
            user_spisok.append(str(var) + '$' + str(role_dct.get(var)) + '$' + str(stat_dct.get(var)) )

        ret_var = spisok_list(user_spisok)

    else:
        ret_var = 'Error'

    return json.dumps(ret_var)


@app.route('/get_stat_in_ses', methods = ['GET'])

def get_stat_in_ses():

    get_id = request.args['idd']
    ses_id = request.args['ses']

    ses_id = str(ses_id)
    get_id = str(get_id)

    local_spisok = []
    stat_spisok = []
    ret_var = ''

    value = id_search(get_id)

    if value == True:

        local_spisok = ses_dct.get(ses_id)

        if get_id in local_spisok:
            local_spisok.remove(get_id)

        for var in local_spisok:
            stat_spisok.append(str(var) + '$' + str(stat_dct.get(var)))

        ret_var = spisok_list(stat_spisok)

    else:
        ret_var = 'Error'

    return json.dumps(ret_var)



@app.route('/get_role_in_ses', methods = ['GET'])

def get_role_in_ses():

    get_id = request.args['idd']
    ses_id = request.args['ses']

    ses_id = str(ses_id)
    get_id = str(get_id)

    local_spisok = []
    role_spisok = []
    ret_var = ''

    value = id_search(get_id)

    if value == True:

        local_spisok = ses_dct.get(ses_id)

        if get_id in local_spisok:
            local_spisok.remove(get_id)

        for var in local_spisok:
            role_spisok.append(str(var) + '$' + str(role_dct.get(var)))

        ret_var = spisok_list(role_spisok)

    else:
        ret_var = 'Error'

    return json.dumps(ret_var)



@app.route('/leave_ses', methods = ['GET']) #Покидание сессии

def leave_ses():

    get_id = request.args['idd']
    ses_id = request.args['ses']

    local_spisok = []
    ret_var = ''

    value = id_search(get_id)

    if value == True:

        local_spisok = ses_dct.get(ses_id)

        if get_id in local_spisok and len(local_spisok) == 1:

            ses_dct.pop(ses_id, None)
            role_dct.pop(get_id, None)
            stat_dct.pop(get_id, None)

            local_spisok.remove(get_id)

            ret_var = True

        else:
            role_dct.pop(get_id, None)
            stat_dct.pop(get_id, None)

            local_spisok.remove(get_id)

            ret_var = True

    else:
        ret_var = 'error'


    return json.dumps(ses_dct)



@app.route('/stat_true', methods = ['GET'])

def stat_true():

    get_id = request.args['idd']
    get_id = str(get_id)

    ret_var = ''

    value = id_search(get_id)

    if value == True:

        stat_dct[get_id] = True
        ret_var = 'True'

    else:
        ret_var = 'Error'

    return json.dumps(ret_var)



@app.route('/get_data', methods = ['GET']) #Получение значений координат других участников, по своему id

def get_data():

    get_id = request.args['idd']
    get_ses = request.args['ses']
    get_coord = request.args['coord']

    get_id = str(get_id)
    get_ses = str(get_ses)
    get_coord = str(get_coord)

    ret_var = ''
    local_dct = {}
    local_spisok = []
    user_spisok = []

    value = id_search(get_id)

    if value == True:

        data_dct[get_id] = get_coord

        user_spisok = ses_dct.get(get_ses)

        local_dct = data_dct.copy()
        local_dct.pop(get_id, None)

        if user_spisok != []:

            for var in user_spisok:
                if local_dct != {} and var != get_id:
                    local_spisok.append(local_dct.get(var))

        ret_var = spisok_list(local_spisok)


    elif value == False:
        ret_var = 'Error'

    else:
        ret_var = None

    return json.dumps(ret_var)



@app.route('/logout', methods = ['GET'])

def logout():

    get_id = request.args['idd']
    get_id = str(get_id)

    value = id_search(get_id)

    if value == True:
        try:
            cur_users.remove(get_id)
        except:
            None

    else:
        None

    return json.dumps(cur_users)


@app.route('/clear_coord', methods = ['GET'])

def clear_coord():

    data_dct.clear()
    ses_dct.clear()
    cur_se.clear()

    return json.dumps(data_dct)

if __name__ == '__main__':
    app.run()
