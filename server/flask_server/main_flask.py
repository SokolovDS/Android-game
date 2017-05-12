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




if __name__ == '__main__':
    app.run()
