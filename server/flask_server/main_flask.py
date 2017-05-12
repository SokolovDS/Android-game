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



#------------------------------------------------------



@app.teardown_appcontext

def close_db(error): #Разрыв соеденения с базой данной

    if hasattr(g, 'game_db'):
        g.game_db.close()



@app.route('/show_users') #Показ базы данных по ссылке, использовалась для тестов, неактивна

def show_users():

    db = get_db()
    cur = db.execute('select email, user_id from users order by id desc')
    users = cur.fetchall()

    #return render_template('show_users.html', users=users)



@app.route('/send_email', methods=['GET'])  #Регистрация по email

def send_email():

    get_email = request.args['email']
    get_email = str(get_email)

    spisok_id = []


    db = get_db()
    cur = db.execute('select * from users')
    all_users = cur.fetchone()

    while all_users is not None:

        if str(all_users[1]) == get_email:
            us_id = str(all_users[2])
            break

        spisok_id.append(str(all_users[2]))

        all_users = cur.fetchone()


    else:
        us_id = randrange(10000, 99999)
        us_id = str(us_id)
        while us_id in spisok_id:
            us_id = randrange(10000, 99999)
            us_id = str(us_id)


        db.execute('insert into users (email, user_id) values ( "{value_1}", "{value_2}" )'.format(value_1 = get_email, value_2 = us_id) )
        db.commit()

    if us_id == '':
        us_id = 'Error'

    return json.dumps(us_id)



@app.route('/get_coord', methods = ['GET']) #Получение значений координат других участников, по своему id

def get_coord():

    get_id = request.args['idd']
    get_coord = request.args['coord']
    get_id = str(get_id)
    get_coord = str(get_coord)

    dct = {}
    local_spisok = []
    ret_var = 'Error'

    db = get_db()
    cur = db.execute('select * from users')
    all_users = cur.fetchone()

    while all_users is not None:

        if str(all_users[2]) == str(get_id):

            file = open('session.txt', 'r')
            text = file.read()
            spisok = text.split()
            file.close()

            for var_1 in range (0, len(spisok), 2):
                dct[spisok[var_1]] = spisok[var_1 + 1]

            dct[get_id] = get_coord

            file = open('session.txt', 'w')
            for var_2 in dct:
                file.write(var_2 + ' ' + dct.get(var_2) + '\n')

            file.close()

            dct.pop(get_id)

            ret_var = ''

            for var_3 in dct:
                local_spisok.append(dct.get(var_3))

            for var_4 in local_spisok:
                ret_var = ret_var + var_4 + '|'

            break

        all_users = cur.fetchone()

    else:
        ret_var = 'Error'


    return json.dumps(ret_var)



@app.route('/logout', methods = ['GET'])

def logout():

    get_id = request.args['idd']
    get_id = str(get_id)

    dct = {}

    file = open('session.txt', 'r')
    text = file.read()
    spisok = text.split()
    file.close()

    for var_1 in range (0, len(spisok), 2):
        dct[spisok[var_1]] = spisok[var_1 + 1]

    dct.pop(get_id, None)

    file = open('session.txt', 'w')
    for var_2 in dct:
        file.write(var_2 + ' ' + dct.get(var_2) + '\n')

    file.close()




if __name__ == '__main__':
    app.run()
