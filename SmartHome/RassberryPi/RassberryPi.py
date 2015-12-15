#coding=utf-8
#!usr/bin/env python

'''
Created on 2015年6月30日

@author: sanhe1
'''

from SmartServer import  SmartServer
import torndb
from deviceSet import deviceSet
from com_session import Session
import logging

# logging.basicConfig(level = logging.DEBUG,
#                     format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt = '%d %b %Y %H:%M:%S',
#                     filename = 'test.log',
#                     filemode = 'w'
#                     )

# logging.info("jflsjfsjflsjlfj")

server = SmartServer()

port_dict = {
            u'一层室内设备通道'  : '/dev/ttyUSB2',
            u'二层室内设备通道'  : '/dev/ttyUSB3',
            u'地下室I/O模块通道' : '/dev/ttyUSB1',
             u'空调外机通道' : '/dev/ttyUSB0',
             }

def HexToString(array):
    snd = ''
    for i in array:
        snd += '%02x' % i
    return snd

sqlConnection = torndb.Connection("127.0.0.1:3306", "smarthome", user = "root", password = "123456")
sql = 'select * from sessions'
mset =  sqlConnection.query(sql)
for item in mset:
    print item['session_name']
    print item['session_id']
    add = deviceSet(item['session_name'])
    line_cmdList = []
    cmdCount = 0
    for cmd in add.getCmdSet():
        print cmd
        cmdCount += 1
        line_cmdList.append({"id" : (++cmdCount), "cmd" : HexToString(cmd), "nbcount" : 0})
#     print port_dict[item['session_name']]
    try :
        print item['session_name'],line_cmdList
        if len(line_cmdList) != 0:
            session = Session(port_dict[item['session_name']], 9600, line_cmdList, 0.5,add)
            server.addSession(port_dict[item['session_name']], session)
    except :
        pass
    
server.start()



    
    