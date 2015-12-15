#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年8月24日

@author: sanhe
'''
from RassberryPi import handlers
from RassberryPi import SmartServer
from Device import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import socket
import fcntl
import struct
import tornado.websocket

def _get_ip_address( ifname):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return socket.inet_ntoa(fcntl.ioctl(
                                        sock.fileno(),
                                        0x8915,  # SIOCGIFADDR
                                        struct.pack('256s', ifname[:15])
                                        )[20:24])
    
    

def handleConnect(sock):
    client = SmartServer.AsyncClient(sock, handlers.handleData)
    SmartServer.SmartServer.client_map[id(client)] = client

if __name__ == "__main__" :
    SmartServer.SmartServer().Init(_get_ip_address('eth0'), 9999,handleConnect)
    SmartServer.SmartServer().Start()
