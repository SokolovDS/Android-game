#Сервер

import socket

req_er = b'req_error'

file_r = open('pos.txt', 'r')
file_str = file_r.readline()
coord = file_str
file_r.close()


mn_api = {'get_chest_position':coord}


s_sock = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM,
                       proto = 0)

s_sock.bind(('', 8080))
s_sock.listen(10)


while True:

    c_sock, c_addr = s_sock.accept()
    print('Подключение установлено', c_addr)
    file_w = open('addr.txt', 'a')
    file_w.write(str(c_addr))
    file_w.close()

    while True:
        
        c_data = c_sock.recv(1024)

        if not c_data:
            break

        c_req = c_data.decode('utf-8')
        c_ans = mn_api.get(c_req)

        if c_ans == None:
            c_sock.sendall(req_er)
        else:
            b_ans = c_ans.encode('utf-8')
            c_sock.sendall(b_ans)

    c_sock.close()



    
    
    
    
    
