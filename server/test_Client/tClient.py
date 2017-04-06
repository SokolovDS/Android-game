#Версия клиента для тестов

import socket

c_sock = socket.socket(socket.AF_INET,
                            socket.SOCK_STREAM)

c_sock.connect(('192.168.1.50', 8080))

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

