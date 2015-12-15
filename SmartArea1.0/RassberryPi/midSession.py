#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年8月14日

@author: sanhe
'''
import asyncore
import socket
import threading
import time

class midSession(asyncore.dispatcher):
    mid_map = {}
    def __init__(self, host, port, session_map = None):
        asyncore.dispatcher.__init__(self)
        self._address = (host,port)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        if session_map is not None:
            self.__class__.mid_map = session_map
        self.buffer = ''
        import struct
        self._heartData = struct.pack('!4i', 0, 0, 0, 0)
        self._interval = 1
        self._heart_timer = threading.Timer(self._interval,self._handle_heartTimer)
        self._reconnect_interval = 5
        self._reconnect_timer = threading.Timer(self._reconnect_interval,self.handle_reconnecttimer)
        self.connect(self._address)
        
        
    def _handle_heartTimer(self):
        print "heartbeat"
        if self.connected:
            self.SendData(self._heartData)
        
    def handle_reconnecttimer(self):
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(self._address)
        
    def handle_connect(self):
        asyncore.dispatcher.handle_connect(self)
        self.mid_map[self._address] = self
        print self._address, "is Connected"
        self._heart_timer.cancel()
        self._heart_timer = threading.Timer(self._interval,self._handle_heartTimer)
        self._heart_timer.start()
        
    def handle_read(self):
        print "handle_read"
        self._heart_timer.cancel()
        self._heart_timer = threading.Timer(self._interval,self._handle_heartTimer)
        self._heart_timer.start()
        buf = self.recv(16)
        if len(buf) == 16 :
            import struct
            head = struct.unpack('!4i',buf)
            print head
        
    def SendData(self, data):
        if self.connected:
            self.buffer = data
            sent = self.send(self.buffer)
            if len(self.buffer) > sent:
                time.sleep(0.1)
                self.SendData(self.buffer[sent:])
                print "SendData : ", self.buffer
            print "Start Heart"
            self._heart_timer.cancel()
            self._heart_timer = threading.Timer(self._interval,self._handle_heartTimer)
            self._heart_timer.start()
            print "End Heart"
        
    def handle_close(self):
        asyncore.dispatcher.handle_close(self)
        if self._address in self.mid_map:
            del self.mid_map[self._address]
            print self._address , "is DisConnected"
        print "handle_close"
        self._reconnect_timer.cancel()
        self._reconnect_timer = threading.Timer(self._reconnect_interval,self.handle_reconnecttimer)
        self._reconnect_timer.start()
        
            
    def handle_connect_event(self):
        try:
            asyncore.dispatcher.handle_connect_event(self)
        except Exception as e:
            print e, self._address
            self.handle_close()
            
            
# if __name__ == "__main__" :
#     session1 = midSession('172.16.1.13',9999)
#     session2 = midSession('172.16.1.13',8888)
# #     asyncore.loop(timeout=10)
#     threading.Thread(target=asyncore.loop).run()