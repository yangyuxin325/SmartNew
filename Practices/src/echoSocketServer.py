import SocketServer


class MyTcpHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        print "Connection address : ",self.client_address
        while True:
            self.data = bytes(self.request.recv(1024).strip())
            print self.data
            self.request.sendall(self.data)
        
        
if __name__ == "__main__":
    HOST,PORT = 'localhost',9999
    server = SocketServer.ThreadingTCPServer((HOST,PORT),MyTcpHandler)
    server.allow_reuse_address = True
    server.serve_forever()