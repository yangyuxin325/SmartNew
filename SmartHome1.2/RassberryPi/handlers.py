#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年8月7日

@author: sanhe
'''
import struct
import json
from protocols import protocolhandlers
import threading

_start_id = 0
_id_mutex = threading.Lock() 
def getUniqueID():
    _id_mutex.acquire()
    global _start_id
    _start_id = _start_id + 1
    if _start_id > 2**32-1:
        _start_id = 0
    _id_mutex.release()
    return _start_id

def handleClientClosed(ip):
    from VideoServer import videoService
    if videoService().setVideoServerState(ip, 0):
        server_name = videoService().getVideoServerName(ip)
        item = {}
        item['server_name'] = server_name
        item['server_ip'] = ip
        item['server_state'] = 0
        item['disk_space'] = videoService().getVideoServerDiskSpace(ip)
        body = {}
        body['member'] = [item,]
        body['local_name'] = videoService().local_name
        body['mac'] = 'mac'
        body['user_name'] = 'user_name'
        body['password'] = 'password'
        body['status_code'] = 255
        encodedjson = json.dumps(body)
        data = struct.pack('!4i{}s'.format(len(encodedjson)), 1, getUniqueID(), 101, len(encodedjson), encodedjson)
        from SmartServer import SmartServer
        for client in SmartServer().client_map.values():
            if client.addr[0] not in videoService().videoservers_map:
                client.SendData(data)

def handleData(client):
    buf = client.recv(16)
    print buf.strip()
    if len(buf) == 16 :
        head = struct.unpack('!4i',buf)
        print head
        if head[3] > 0 :
            buf = client.recv(head[3])
            if len(buf) == head[3] :
                body = json.loads(buf)
                print body
                #         com_handlers.doSessionState(self, 1)
                try:
                    protocolhandlers[head[2]](head, body, client)
                except Exception as e:
                    print "handleData got Error : ", e
    
#数据通道连接状态改变
def hanldeSessionState(data):
    print "hanldeSessionState : ", data, type(data)
    from SmartServer import SmartServer
    if data['session_state'] == 1 :
        SmartServer().dataSession_map[data['session_name']].setState(True)
    else:
        SmartServer().dataSession_map[data['session_name']].setState(False)
    try: 
        head = range(4)
        head[0] = 1
        head[1] = getUniqueID()
        head[2] = 8
        head[3] = 0
        body ={}
        state = data['session_state']
        print "hanldeSessionState : TYPETYPETYPETYPE", type(state)
        name = data['session_name']
        body['session_state'] = state
        body['session_name'] = name
        body['local_name'] = u'西山游泳馆'
        body['mac'] = ""
        body['user_name'] = 'user_name'
        body['password'] = 'password'
        body['status_code'] = 255
        encodedjson = json.dumps(body)
        head[3] = len(encodedjson)
        data = struct.pack('!4i{}s'.format(head[3]),head[0],head[1],head[2],head[3],encodedjson)
        print 'hanldeSessionState : SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS', data[16:]
    except Exception as e:
        print "handleSessionState ERROR ERROR ERROR ERROR", e
    for client in SmartServer().client_map.values():
#         if client.tellFlag():
        client.SendData(data)
     
# 数据通道上的数据有变化
def handleDataChanged(data):
#     print "handleDataChanged :" ,data, type(data)
    try :
        head = range(4)
        head[0] = 1
        head[1] = getUniqueID()
        head[2] = 9
        head[3] = 0
        body = {}
        body['member'] = data['data']
        body['dev_name'] = data['dev_name']
        body['session_name'] = data['session_name']
        body['mac'] = ""
        body['user_name'] = 'user_name'
        body['password'] = 'password'
        body['status_code'] = 255
        encodedjson = json.dumps(body)
        head[3] = len(encodedjson)
        data = struct.pack('!4i{}s'.format(head[3]), head[0], head[1], head[2], head[3], encodedjson)
    except Exception as e:
        print "handleDataChanged got Error : ", e
    from SmartServer import SmartServer
    for client in SmartServer().client_map.values():
        print  "Client UPLOAD FALG IS ", client.tellFlag()
        if client.tellFlag():
            client.SendData(data)
            print "handleDataChanged has Send : ", data[16:]
    
def handleRequest(data):
    try : 
        from SmartServer import SmartServer
        client = SmartServer().client_map[data['client_id']]
        head = list(data['head'])
        body = data['body']
        body['status_code'] = 2
        encodedjson = json.dumps(body)
        head[3] = len(encodedjson)
        print "handle Request MSGBODY LENGTH: ", head[3]
        data = struct.pack('!4i{}s'.format(head[3]),head[0],head[1],head[2],head[3],encodedjson)
        client.SendData(data)
    except Exception as e:
        print "handleRequest got Error: ", e
    
def handleDeviceData(data):
    if data['data']:
        for key, value in data['data'].getDataDict().items():
            print key, value


def getDeviceData(datasession, data):
    print "getDeviceData : ", data
    try :
        dev = datasession.getDevice(data['data']['body']['dev_name'])
        if dev:
            member = []
            for value in dev.getDataDict().values():
                member.append(value.getDataItem())
                print "GETDEVICEDATA ITEM WWWWW: ", value
                print "GETDEVICEDATA ITEM WWWWW: ", value.getDataItem()
            print "getDeviceData :", member
            data['data']['body']['member'] = member
        data['data']['body']['status_code'] = 2
        datasession.putResultQueue(handleRequest,data['data'])
    except Exception as e:
        print "getDeviceData got Error: ", e
#     for key,value in dev.getDataDict().items():
#             print key, value
    
def sendDeviceCmd(datasession, data):
    print "sendDeviceCmd: ", data
    datasession.AddSendCmd(data['data'],0)
    
def sessStartOrStop(datasession, data):
    print "sessStartOrStop : " , data
    if 0 == data['data']['state'] :
        datasession.stop()
        print "sessStartOrStop : ",datasession.State()
        
def getSessState(datasession, data):
    print "getSessState : ", data
    if datasession.State() == True :
        data['data']['body']['session_state'] = 1
    else:
        data['data']['body']['session_state'] = 0
    data['data']['body']['status_code'] = 2
    datasession.putResultQueue(handleRequest,data['data'])
    

    
#调用data_session的putTaskQueue运行handler
MsgDict = {
           1 : getDeviceData,
           2 : sendDeviceCmd,
           3 : sessStartOrStop,
           4 : getSessState,
           }
