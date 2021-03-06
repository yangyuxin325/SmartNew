#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年8月7日

@author: sanhe
'''
import handlers
from MasterPro.SmartServer import SmartServer
from MasterPro.SmartServer import sock_sessionA
from MasterPro.SmartServer import AsyncClient
from Device import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')



def handleConnect(sock):
    if sock.addr[0] in SmartServer.ip_ServerPara:
        server_para = SmartServer.ip_ServerPara[sock.addr[0]]
        if server_para.Server_Type() == 'area' or server_para.Server_Type() == 'node':
            session = sock_sessionA(server_para,sock,handlers.handleData,SmartServer.name_sockSesssion)
            SmartServer.name_sockSesssion[session.Server_Name()] = session
            flag = False
            if SmartServer().workflag:
                if server_para.Server_Type() == 'area':
                    SmartServer.name_sockSesssion[session.Server_Name()].init_data('area',server_para.Server_Ip())
                    for node_name,unit_name in SmartServer.nodeunit_map:
                        if unit_name == server_para.Server_Name():
                            server_para = SmartServer.name_sessServer['area']
                            SmartServer.name_sockSesssion[node_name].init_data('area',server_para.Server_Ip())
                            SmartServer.name_sockSesssion[node_name].handle_close()
                    SmartServer.name_sockSesssion[SmartServer()._sessServer.Server_Name()].initData('area',server_para.Server_Ip())
                else:
                    SmartServer.name_sockSesssion[server_para.Server_Name()].initData(
                            SmartServer.nodeunit_map[server_para.Server_Name()],server_para.Server_Ip())
            else:            
                if server_para.Server_Type() == 'area':
                    SmartServer.name_sockSesssion[session.Server_Name()].init_data('area',server_para.Server_Ip())
                else:
                    flag = True
                    for node_name,unit_name in SmartServer.nodeunit_map:
                        if unit_name == server_para.Server_Name():
                            if node_name not in SmartServer.name_sockSesssion:
                                flag = False
            if flag and 'area' in SmartServer.name_sockSesssion:
                for node_name,unit_name in SmartServer.nodeunit_map:
                    if unit_name == server_para.Server_Name():
                        server_para = SmartServer.name_sessServer['area']
                        SmartServer.name_sockSesssion[node_name].init_data('area',server_para.Server_Ip())
                SmartServer.name_sockSesssion[SmartServer()._para.Server_Name()].initData('area',server_para.Server_Ip())
                SmartServer().start_work()
        else:
            client = AsyncClient(sock, handlers.handleData)
            SmartServer.client_map[id(client)] = client
            
if __name__ == "__main__" :
    SmartServer().Init('172.16.1.13', 9999, handleConnect)
    SmartServer().Start()