#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年8月24日

@author: sanhe
'''
from RassberryPi import handlers
from RassberryPi import SmartServer
from Device import *
from RassberryPi.handlers import handleAskInitData
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
    SmartServer.SmartServer().client_map[id(client)] = client
    
def handleTimer():
    print "unit_node", "handleTimer"
    if SmartServer.SmartServer().area_connection is not None:
        return
    SmartServer.SmartServer().allChannelStart()
    
def handleConnectUnit(sock):
    client = SmartServer.AsyncClient(sock, handlers.handleDataUnit)
    SmartServer.SmartServer.client_map[id(client)] = client
    if cmp(client.addr[0], SmartServer.SmartServer().area_ip) == 0:
        SmartServer.SmartServer().stopAllChannels()
        handleAskInitData(client)

def handleConnectArea(sock):
    client = SmartServer.AsyncClient(sock, handlers.handleDataArea)
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
    import torndb
    server_ip = _get_ip_address('eth0')
    
    conn = torndb.Connection(SmartServer.SmartServer().db_addr, SmartServer.SmartServer().db_name,
                              user = SmartServer.SmartServer().db_user, password = SmartServer.SmartServer().db_password)
    sql = "select server_ip from machines where server_type = %s"
    SmartServer.SmartServer().area_ip = conn.query(sql, 'area')[0]["server_ip"]
    sql = "select server_type from machines where server_ip = %s"
    data_set = conn.query(sql, server_ip)
    conn.close()
#     data_set[0]['server_type'] = 'node'
    if len(data_set) > 0:
        if data_set[0]['server_type'] == 'unit_node':
            SmartServer.SmartServer().Init(server_ip, 9999,handleConnectUnit)
            SmartServer.SmartServer().Start()
        #     启动定时，如果定时时间范围内，区域已经连接则退出，否则启动巡检
            import threading
            th = threading.Timer(5,handleTimer)
            th.start()
        elif data_set[0]['server_type'] == 'area':
            from RassberryPi.VideoServer import videoService
            videoService().Init(u"西山游泳馆")
            SmartServer.SmartServer().Init(server_ip, 9999,handleConnectArea)
            SmartServer.SmartServer().Start()
        elif data_set[0]['server_type'] == 'node':
            SmartServer.SmartServer().Init(server_ip, 9999,handleConnect)
            SmartServer.SmartServer().Start()
