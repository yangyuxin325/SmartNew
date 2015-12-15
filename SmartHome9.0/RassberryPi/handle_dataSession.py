#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年8月3日

@author: sanhe
'''
import os

def handleDeviceData(data):
    print os.getpid(),"handleDeviceData :" ,data['dev_name']
    if data['data']:
        for key, value in data['data'].getDataDict().items():
            print key, value

def getDeviceData(datasession, data):
    print os.getpid(),"getDeviceData", data
    if datasession.getDevice(data['dev_name']) :
        data['data'] = datasession.getDevice(data['dev_name'])
    else:
        data['data'] = None
    print os.getpid(),data
    for key,value in data['data'].getDataDict().items():
            print key, value
#     datasession.putResultQueue(handleDeviceData,data)
#     datasession.closeSerial()
#     import time
#     time.sleep(3)
#     datasession.putTaskQueue({'MsgType' : 1 ,'dev_name' : u'室外北区红外'})
#     datasession.start()
    
def sendDeviceCmd(datasession, data):
    print "sendDeviceCmd: ", data
    datasession.AddSendCmd(data['data'],0)
    
def sessStartOrStop(datasession, data):
    print "sessStartOrStop: ", data
    if 1 == data['state'] :
        datasession.start()
    else:
        datasession.stop()

MsgDict = {
           1 : getDeviceData,
           2 : sendDeviceCmd,
           3 : sessStartOrStop,
           }

# lambda datasession, data : MsgDict[data['MsgType']](datasession,data)
# 
# def handleTask(datasession, data):
#     MsgDict[data['MsgType']](datasession,data)
