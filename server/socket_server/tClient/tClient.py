#Версия клиента для тестов

import socket

serv_ip ='192.168.1.50' # ip сервера внутри сети
                        #Для теста введите ip компьютера на котором
                        #расположен сервер внутри вашей сети

c_sock = socket.socket(socket.AF_INET,
                            socket.SOCK_STREAM)

c_sock.connect((serv_ip, 8080))

while True:
    c_dt = input('Q: ')
    if c_dt == 'end':
        c_sock.close()
        break
    
    b_dt = c_dt.encode('utf-8')
    c_sock.sendall(b_dt)
    s_dt = c_sock.recv(1024)
    print('A:', s_dt.decode('utf-8'))
    print('')
          
c_sock.close()

