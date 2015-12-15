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

    
def getSerialCOM():
    import commands;
    comArr = []
    status, str1 = commands.getstatusoutput('ls /dev/serial/by-path')
    if status == 0:
        arr = str1.splitlines()
        for strtemp in arr:
            cmd = "ls -la /dev/serial/by-path | grep " + strtemp + " | cut -d '/' -f3"
            comArr.append(commands.getoutput(cmd))
        return comArr

if __name__ == "__main__" :
    print getSerialCOM()
    SmartServer.SmartServer().Init(_get_ip_address('eth0'), 9999,handleConnect)
    SmartServer.SmartServer().Start()
    from RassberryPi.VideoServer import videoService
    videoService().Init(u"西山游泳馆")
