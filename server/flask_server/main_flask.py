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

        for var in range(len(local_spisok)):

            if var_2 == len(local_spisok) - 1 or var_2 == 0:
                ret_var = ret_var + local_spisok[var_2]

            elif var_2 != len(local_spisok) - 1:
                ret_var = ret_var + local_spisok[var_2] + '|'


    return ret_var

#------------------------------------------------------


global coord_dct; coord_dct = {}
global cur_users; cur_users = {}
global cur_ses; cur_ses = {}

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
        cur_users[ret_var] = ''

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

        if cur_ses != {}:

            for var_1 in cur_ses:
                local_spisok.append(str(var_1))

            ret_var = spisok_list(local_spisok)

        else:
            ret_var = '0'

    else:
        ret_var = 'Error'

    return json.dumps(ret_var)


@app.route('/get_coord', methods = ['GET']) #Получение значений координат других участников, по своему id

def get_coord():

    get_id = request.args['idd']
    get_coord = request.args['coord']

    get_id = str(get_id)
    get_coord = str(get_coord)

    ret_var = ''
    local_dct = {}
    local_spisok = []

    value = id_search(get_id)

    if value == True:

        coord_dct[get_id] = get_coord

        local_dct = coord_dct.copy()
        local_dct.pop(get_id, None)

        for var in local_dct:
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


    return json.dumps('True')


@app.route('/clear_coord', methods = ['GET'])

def clear_coord():

    coord_dct.clear()

    return json.dumps(coord_dct)

if __name__ == '__main__':
    app.run()
