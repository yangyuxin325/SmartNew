import socket

HOST = ''
PORT = 9999
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))

while True:
    senddata = raw_input("Please input senddata: ")
    if senddata == 'quit':
        break
    else:
        s.sendall(senddata)
        recvdata = s.recv(1024)
        print "Received : ", recvdata
s.close()