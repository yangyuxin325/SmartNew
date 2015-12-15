#coding=utf-8
#!/usr/bin/env python

'''
Created on 2015年3月2日

@author: sanhe
'''
from com_session import Session
import serial.tools.list_ports
from SmartServer import SmartServer
from SmartConfig import Serial_DevCmdSet_Config
import CommonInterface
import time
from threading import Timer

startTime = time.time()

def handleTimer():
    print time.time() - startTime
#     SmartServer().getSession('/dev/ttyUSB0').addDataItem({"id" : 999, "cmd" : "1506000d0001dadd", "nbcount" : 0})
#     SmartServer().stop()

if __name__ == '__main__':

    port_list = list(serial.tools.list_ports.comports())
    for i in range(len(port_list)):
        print port_list[i][0]
#     print port_list

    server = SmartServer()
    for key,value in Serial_DevCmdSet_Config.items():
        session = Session(key, 9600, value, 0.5)
        server.addSession(key, session)
        
    server.start()
    
#     print Dev_CmdPack.infraredCmdPack(21,6,7,1)
    timer = Timer(5,handleTimer)
#     timer.start()
    
#     for item in Serial_Dev_Config['/dev/ttyUSB1'] :
#         print item
#         
# #     Dev_CmdPack.CmdPackConfig[item[0]]
#     print Dev_CmdPack.plc_mokuaiCmdPack(1, 3, 2)
#     
# #     CommonInterface.SendHardCMD('/dev/ttyUSB1', '010101')
#     
#     data_list.insert(0,"")
#     print data_list
    

    

    
    

