#Сервер

#Библиотеки для работы сервера
from flask import Flask, request, json

#Сторонние библиотеки
#import math

#Файлы дополнительных скриптов
import distantion

app = Flask(__name__)



@app.route("/send_position", methods = ['GET'])

def send_position():

    phone_position = request.args['coord']

    chest_position = '56.843927|60.653151'

    dist = distantion.calc(chest_position, phone_position)

    return json.dumps(dist)


if __name__ == '__main__':
    app.run()
