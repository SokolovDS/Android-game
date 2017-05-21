#Скрипт регистрации, авторизации и теста сервера

import requests
import time



url_1 = 'http://artkholl.pythonanywhere.com/send_email?email={value_1}'
url_2 = 'http://artkholl.pythonanywhere.com/get_coord?idd={value_2}&coord={value_3}'
url_3 = 'http://artkholl.pythonanywhere.com/logout?idd={value_4}'

try:
    file = open('email.txt','r')

except FileNotFoundError:
    
    email = input('Введите ваш email: ')
    file = open('email.txt','w')
    file.write(email)

else:
    email = file.read()
    
    
finally:
    file.close()

req_url_1 = url_1.format(value_1 = email)
req_1 = requests.get(req_url_1)
idd = req_1.json()

text = input('Введите фразу которую собираетесь отправлять: ')

req_url_2 = url_2.format(value_2 = idd, value_3 = text)

for var in range(10):
    time.sleep(2)
    req_2 = requests.get(req_url_2)
    ans = req_2.json()
    print('\n',ans)

else:
    req_url_3 = url_3.format(value_4 = idd)
    requests.get(req_url_3)
    
