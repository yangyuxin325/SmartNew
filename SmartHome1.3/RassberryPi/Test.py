#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年8月14日

@author: sanhe
'''
import handlers
import SmartServer
import torndb
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from data_session import data_session

def handleConnect(sock):
    client = SmartServer.AsyncClient(sock, handlers.handleData)
    SmartServer.SmartServer.client_map[id(client)] = client

if __name__ == "__main__" :
#     session = data_session( u'空调外机通道' , '/dev/ttyUSB0', 9600, 0.5, 
#                                                     lambda self, data : handlers.MsgDict[data['MsgType']](self,data))
# #     session.start()
#     for value in session.getDevice(u'室外北区红外').getDataDict().values():
#         print value.getDataItem()
    conn = torndb.Connection("127.0.0.1:3306", "smarthome", user = "root", password = "123456")
    sql = 'select server_type from machines where server_ip = %s'
    data_links = conn.query(sql,'172.16.1.13')
    print data_links,"AAAAA"
    sql = 'select link_key,link_type,link_para1 from conf_links where conf_name = %s'
    sql = 'select conf_name,description from infrared_confs'
    data_links = None
    try :
        data_links = conn.query(sql)
    except Exception as e:
        print e
    print data_links
    conn.close()
#     SmartServer.SmartServer().Init('172.16.1.13', 8888, handleConnect)
#     SmartServer.SmartServer().Start()