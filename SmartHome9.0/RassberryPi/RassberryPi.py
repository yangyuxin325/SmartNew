#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年8月7日

@author: sanhe
'''
import handlers
import SmartServer
from Device import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def handleConnect(sock):
    client = SmartServer.AsyncClient(sock, handlers.handleData)
    SmartServer.SmartServer.client_map[id(client)] = client

if __name__ == "__main__" :
    SmartServer.SmartServer().Init('172.16.1.13', 9999, handleConnect)
    SmartServer.SmartServer().Start()