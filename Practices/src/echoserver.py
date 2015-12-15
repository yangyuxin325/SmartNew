import socket
from time import sleep

HOST = ''
PORT = 9999
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(5)

while True:
    conn,addr = s.accept()
    
    print 'Connect by',addr
    
    while True:
        data = conn.recv(1024)
        if not data: 
            sleep(1.5)
            continue
        print data
        conn.sendall(data)
conn.close()