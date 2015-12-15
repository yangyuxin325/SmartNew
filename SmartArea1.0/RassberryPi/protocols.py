#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年8月19日

@author: sanhe
'''
import json
import struct
import torndb

protocolhandlers = {}

def handleDeviceTypes(head, body, client):
    head = list(head)
    if body['status_code'] == 1:
        from Device.device import device_Dict
        member = []
        for dev_type,description in device_Dict.items():
            item = {}
            item['dev_type'] = dev_type
            item['description'] = description
            member.append(item)
        body['member'] = member
        body['status_code'] = 2
        encodedjson = json.dumps(body)
        head[3] = len(encodedjson)
        data = struct.pack('!4i{}s'.format(head[3]),head[0],head[1],head[2],head[3],encodedjson)
        client.SendData(data)
        
def handleSessionTypes(head, body, client):
    head = list(head)
    if body['status_code'] == 1:
        member = []
        item = {}
        item['session_type'] = 1
        item['description'] = 'usb转485'
        member.append(item)
        body['member'] = member
        body['status_code'] = 2
        encodedjson = json.dumps(body)
        head[3] = len(encodedjson)
        data = struct.pack('!4i{}s'.format(head[3]),head[0],head[1],head[2],head[3],encodedjson)
        client.SendData(data)

def handleUnits(head, body, client):
    head = list(head)
    if body['status_code'] == 1:
        member = []
        item = {}
        item['unit_name'] = u'单元服务器1'
        item['unit_ip'] = '172.16.1.13'
        member.append(item)
        body['member'] = member
        body['status_code'] = 2
        print body
        encodedjson = json.dumps(body)
        head[3] = len(encodedjson)
        data = struct.pack('!4i{}s'.format(head[3]),head[0],head[1],head[2],head[3],encodedjson)
        client.SendData(data)
        
def handleNodes(head, body, client):
    head = list(head)
    if body['status_code'] == 1:
        member = []
        item = {}
        item['node_name'] = '节点服务器1'
        item['node_ip'] = '172.16.1.13'
        member.append(item)
        body['member'] = member
        body['status_code'] = 2
        encodedjson = json.dumps(body)
        head[3] = len(encodedjson)
        data = struct.pack('!4i{}s'.format(head[3]),head[0],head[1],head[2],head[3],encodedjson)
        client.SendData(data)
        
def handleSessions(head, body, client):
    head = list(head)
    if body['status_code'] == 1:
        sqlConnection = torndb.Connection("127.0.0.1:3306", "smarthome", user = "root", password = "123456")
        sql = 'select * from sessions'
        mset =  sqlConnection.query(sql)
        sqlConnection.close()
        body['member'] = mset
        body['status_code'] = 2
        encodedjson = json.dumps(body)
        head[3] = len(encodedjson)
        data = struct.pack('!4i{}s'.format(head[3]),head[0],head[1],head[2],head[3],encodedjson)
        client.SendData(data)
        
def handleDevices(head, body, client):
    head = list(head)
    if body['status_code'] == 1:
        sqlConnection = torndb.Connection("127.0.0.1:3306", "smarthome", user = "root", password = "123456")
        sql = 'select dev_name,dev_type,dev_id from devices Where session_name = %s'
        mset =  sqlConnection.query(sql, body['session_name'])
#         print mset
        sqlConnection.close()
        body['member'] = mset
        body['status_code'] = 2
        print body
        encodedjson = json.dumps(body)
        head[3] = len(encodedjson)
        data = struct.pack('!4i{}s'.format(head[3]),head[0],head[1],head[2],head[3],encodedjson)
        client.SendData(data)
        
def handleDevArea(head, body, client):
    head = list(head)
    sqlConnection = torndb.Connection("127.0.0.1:3306", "smarthome", user = "root", password = "123456")
    if body['status_code'] == 1:
        sql = 'select area from areas Where dev_name = %s'
        mset =  sqlConnection.query(sql, body['dev_name'])
        if len(mset) != 0:
            body['area_name'] = mset[0]['area']
        body['status_code'] = 2
        encodedjson = json.dumps(body)
        head[3] = len(encodedjson)
        data = struct.pack('!4i{}s'.format(head[3]),head[0],head[1],head[2],head[3],encodedjson)
        client.SendData(data)
    elif body['status_code'] == 3:
        pass
    elif body['status_code'] == 6:
        pass
    sqlConnection.close()
    
def handleSessionState(head, body, client):
    head = list(head)
    if body['status_code'] == 1:
        body['session_state'] = 0
        from SmartServer import SmartServer
        if body['session_name'] in SmartServer().dataSession_map:
            if SmartServer().dataSession_map[body['session_name']].State() :
                body['session_state'] = 1
        body['status_code'] = 2
        print "handleSessionState : " , body
        encodedjson = json.dumps(body)
        head[3] = len(encodedjson)
        data = struct.pack('!4i{}s'.format(head[3]),head[0],head[1],head[2],head[3],encodedjson)
        client.SendData(data)
    
def handleDevDatas(head, body, client):
    head = list(head)
    if body['status_code'] == 1:
        from SmartServer import SmartServer
        if SmartServer().putTask(body['session_name'], 
                                 {'MsgType' : 1, 'data' : {'client_id' : id(client),'head' : head, 'body' : body}}) is False:
            body['session_state'] = 0
            body['status_code'] = 2            
            encodedjson = json.dumps(body)
            head[3] = len(encodedjson)
            data = struct.pack('!4i{}s'.format(head[3]),head[0],head[1],head[2],head[3],encodedjson)
            client.SendData(data)
    elif body['status_code'] == 2:
        pass
    
def handleStartUpload(head, body, client):
    head = list(head)
    if body['status_code'] == 1:
        client.Start_tell()
        print "handleStartUpload is ", client.tellFlag()
        body['status_code'] = 2
        encodedjson = json.dumps(body)
        head[3] = len(encodedjson)
        data = struct.pack('!4i{}s'.format(head[3]),head[0],head[1],head[2],head[3],encodedjson)
        client.SendData(data)
    
def handleDevTypeBaseDatas(head, body, client):
    head = list(head)
    if body['status_code'] == 1:
        table_name = body['dev_type'] + '_conf'
        sqlConnection = torndb.Connection("127.0.0.1:3306", "smarthome", user = "root", password = "123456")
        sql = 'Select conf_name, description from ' + table_name
        mset = []
        try :
            mset =  sqlConnection.query(sql, body['dev_name'])
        except Exception as e:
            print "handleDevTypeBaseDatas got Error : " , e
        if len(mset) > 0 :
            body['member'] = mset
        body['status_code'] = 2
        encodedjson = json.dumps(body)
        head[3] = len(encodedjson)
        data = struct.pack('!4i{}s'.format(head[3]),head[0],head[1],head[2],head[3],encodedjson)
        client.SendData(data)
        sqlConnection.close()

def handleDataProperties(head, body, client):
    head = list(head)
    if body['status_code'] == 1:
        pass
    
def handleControlSession(head, body, client):
    head = list(head)
    print "handleControlSession : ", body
    if body['status_code'] == 1:
        from SmartServer import SmartServer
        if body['session_state'] == 0:
            SmartServer().putTask(body['session_name'], {'MsgType' : 3, 'data' : {'state' : body['session_state']}})
        elif body['session_state'] == 1:
            if SmartServer().startOldSession(body['session_name']) is False :
                SmartServer().channelStart(body['session_name'])
        elif body['session_state'] == 2 :
            SmartServer().channelStart(body['session_name'])
        body['status_code'] = 2
        print "handleControlSession : " , body
        encodedjson = json.dumps(body)
        head[3] = len(encodedjson)
        data = struct.pack('!4i{}s'.format(head[3]),head[0],head[1],head[2],head[3],encodedjson)
        client.SendData(data)
        
def handleVideoServers(head, body, client):
    from VideoServer import videoService
    from SmartServer import SmartServer
    from handlers import getUniqueID
    import copy
    head = list(head)
    body1 = None
    if body['status_code'] == 1:
        if body['member']:
            print "member is not None :" ,body
            for item in body['member']:
                if item['server_ip'] is not None:
                    if videoService().addVideoServer(item['server_ip'],item['disk_space'],1):
                        body['status_code'] = 255
                        encodedjson1 = json.dumps(body)
                        dataUpload = struct.pack('!4i{}s'.format(len(encodedjson1)), 1, getUniqueID(), head[2], len(encodedjson1), encodedjson1)
                        for client1 in SmartServer().client_map.values():
                            if client1.addr[0] not in videoService().videoservers_map:      
                                client1.SendData(dataUpload)
                    else:
                        server_name = videoService().getVideoServerName(item['server_ip'])
                        if server_name:
                            item['server_name'] = server_name
                            body['member'] = [item,]
#                         添加IP核对
                        if videoService().updateVideoServerDiskSpace(item['server_ip'], item['disk_space']):
                            m = 1
#                             更新数据库
                        if videoService().getVideoServerState(item['server_ip']) == 0 :
                            videoService().setVideoServerState(item['server_ip'], 1)
                            item1 = {}
                            item1['server_name'] = server_name
                            item1['server_ip'] = item['server_ip']
                            item1['server_state'] = 1
                            item1['disk_space'] = videoService().getVideoServerDiskSpace(item['server_ip'])
                            body1 = {}
                            body1['member'] = [item1,]
                            body1['local_name'] = videoService().local_name
                            body1['mac'] = 'mac'
                            body1['user_name'] = 'user_name'
                            body1['password'] = 'password'
                            body1['status_code'] = 255
                            encodedjson1 = json.dumps(body1)
                            dataUpload = struct.pack('!4i{}s'.format(len(encodedjson1)), 1, getUniqueID(), 101, len(encodedjson1), encodedjson1)
                            for client1 in SmartServer().client_map.values():
                                if client1.addr[0] not in videoService().videoservers_map:      
                                    client1.SendData(dataUpload)
                            body1 = None
        else :
            print "member is None :" ,body
            member = []
            for server_ip , videoserver in videoService().videoservers_map.items():
                item ={}
                item['server_ip'] = server_ip
                item['server_name'] = videoserver.getName()
                item['server_state'] = videoserver.State()
                item['disk_space'] = videoserver.getDiskSpace()
                member.append(item)
                body['member'] = member
#                 print "handleVideoServers :", member
            if len(member) == 0:
                body['member'] = None
        body['status_code'] = 2
        body['local_name'] = videoService().local_name
    elif body['status_code'] == 3:
        if 1 == len(body['member']):
            item = body['member'][0]
            if videoService().updateVideoServerName(item['server_ip'], item['server_name']):
                body['status_code'] = 4
                body1 = copy.deepcopy(body)
                body1['status_code'] = 256
    #             向数据库中添加或修改
            else:
                body['status_code'] = 5    
        else:
            body['status_code'] = 5
        body['local_name'] = videoService().local_name
    elif body['status_code'] == 6:
        if 1 == len(body['member']):
            item = body['member'][0]
            if videoService().delVideoServer(item['server_name']):
                body['status_code'] = 7
                body1 = copy.deepcopy(body)
                body1['status_code'] = 257
    #             从数据库中删除
            else:
                body['status_code'] = 8
        else:
            body['status_code'] = 8
    print "handleVideoServers : ", body
    encodedjson = json.dumps(body)
    head[3] = len(encodedjson)
    data = struct.pack('!4i{}s'.format(head[3]),head[0],head[1],head[2],head[3],encodedjson)
    client.SendData(data)
    if body1 is not None:
        encodedjson = json.dumps(body1)
        head[3] = len(encodedjson)
        data = struct.pack('!4i{}s'.format(head[3]),head[0],getUniqueID(),head[2],head[3],encodedjson)
        for client1 in SmartServer().client_map.values():
            if client1.addr[0] not in videoService().videoservers_map:
                print client1.addr
                if cmp(client1.addr[0], client.addr[0]) != 0:
                    client1.SendData(data)
    
def handleVideoIPCS(head, body, client):
    head = list(head)
    from VideoServer import videoService
    from SmartServer import SmartServer
    from handlers import getUniqueID
    import copy
    body1 = None
    if body['status_code'] == 1:
        member = []
        videoserver = videoService().getVideoServer(body['server_name'])
        if videoserver is not None:
            for name , ipc in videoserver.getIPCs().items():
                item = ipc.GetIPCProperties()
                item['name'] = name
                member.append(item)
        if len(member) == 0:
            member = None
        body['member'] = member
        body['status_code'] = 2
    elif body['status_code'] == 3:
        videoserver = videoService().getVideoServer(body['server_name'])
        if videoserver is not None:
            if 1 == len(body['member']):
                item = body['member'][0]
                from VideoServer import VideoIPC
                ipc = VideoIPC(item['ip'],item['url'],item['fps'],item['resolution'],item['streamsize'])
                if videoService().addVideoIPC(videoserver.getIp(), item['name'],ipc):
                    body['status_code'] = 4
                    body1 = copy.deepcopy(body)
                    body1['status_code'] = 256
#                     向数据库中添加
                else:
                    ipc = videoserver.getIPCs()[item['name']]
                    if ipc and ipc.getProperty('ip') == item['ip']:
                        videoService().updateIPCProperty(videoserver.getIp(), item['name'], 'url', item['url'])
                        videoService().updateIPCProperty(videoserver.getIp(), item['name'], 'fps', item['fps'])
                        videoService().updateIPCProperty(videoserver.getIp(), item['name'], 'resolution', item['resolution'])
                        videoService().updateIPCProperty(videoserver.getIp(), item['name'], 'streamsize', item['streamsize'])
                        body['status_code'] = 4
                        body1 = copy.deepcopy(body)
                        body1['status_code'] = 256
#                         更改数据库
                    else:
                        body['status_code'] = 5
            else:
                body['status_code'] = 5
        else:
            body['status_code'] = 5
    elif body['status_code'] == 6:
        videoserver = videoService().getVideoServer(body['server_name'])
        if videoserver is not None:
            if 1 == len(body['member']):
                item = body['member'][0]
                if videoService().delVideoIPC(videoserver.getIp(), item['name']):
                    body['status_code'] = 7
                    body1 = copy.deepcopy(body)
                    body1['status_code'] = 257
#                     从数据库中删除
                else:
                    body['status_code'] = 8
            else:
                body['status_code'] = 8
        else:
            body['status_code'] = 8
    print "handleVideoIPCS : ", body
    encodedjson = json.dumps(body)
    print encodedjson
    head[3] = len(encodedjson)
    data = struct.pack('!4i{}s'.format(head[3]),head[0],head[1],head[2],head[3],encodedjson)
    client.SendData(data)
    if body1 is not None:
        encodedjson = json.dumps(body1)
        head[3] = len(encodedjson)
        data = struct.pack('!4i{}s'.format(head[3]),head[0],getUniqueID(),head[2],head[3],encodedjson)
        for client1 in SmartServer().client_map.values():
            if client1.addr[0] not in videoService().videoservers_map:
                if client1.addr[0] != client.addr[0]:
                    client1.SendData(data)
    
    
def handleVideoRecords(head, body, client):
    head = list(head)
    from VideoServer import videoService
    from SmartServer import SmartServer
    from handlers import getUniqueID
    import copy
    body2 = None
    if body['status_code'] == 1:
        member = []
        server_name = None
        for item in body['member']:
            server_name = item['server_name']
            videoserver = videoService().getVideoServer(server_name)
            item['savedays'] = videoserver.GetRecordSaveDays()
            member.append(item)
        body['member'] = member
        body['local_name'] = videoService().local_name
        body['status_code'] = 2
    elif body['status_code'] == 3:
        if 1 == len(body['member']):
            item = body['member'][0]
            if videoService().updateVideoSeverRecordDays(item['server_name'], item['savedays']):
                body['status_code'] = 4
                body2 = copy.deepcopy(body)
                body2['status_code'] = 256
#                 更改数据库
            else:
                body['status_code'] = 5
        else:
            body['status_code'] = 5
    print "handleVideoRecords : ", body
    encodedjson = json.dumps(body)
    head[3] = len(encodedjson)
    data = struct.pack('!4i{}s'.format(head[3]),head[0],head[1],head[2],head[3],encodedjson)
    client.SendData(data)
    if body2 is not None:
        encodedjson = json.dumps(body2)
        head[3] = len(encodedjson)
        data = struct.pack('!4i{}s'.format(head[3]),head[0],getUniqueID(),head[2],head[3],encodedjson)
        for client1 in SmartServer().client_map.values():
            if client1.addr[0] not in videoService().videoservers_map:
                if cmp(client1.addr[0], client.addr[0]) != 0:
                    client1.SendData(data)
            
        
        
def handleVideoServiceState(head, body, client):
    head = list(head)
    from VideoServer import videoService
    from SmartServer import SmartServer
    from handlers import getUniqueID
    if body['status_code'] == 1:
        member = []
        for item in body['member']:
            flag = videoService().getVideoServerStartFlag(item['server_name'])
            item['service_state'] = flag
            member.append(item)
        body['status_code'] = 2
        encodedjson = json.dumps(body)
        head[3] = len(encodedjson)
        data = struct.pack('!4i{}s'.format(head[3]),head[0],head[1],head[2],head[3],encodedjson)
        client.SendData(data)
        print   "handleVideoServiceState: ", body
    elif body['status_code'] == 2:
        print body
    elif body['status_code'] == 255:
        item = body['member'][0]
        videoService().setVideoServerStartFlag(item['server_name'], item['service_state'])
        encodedjson = json.dumps(body)
        head[3] = len(encodedjson)
        data = struct.pack('!4i{}s'.format(head[3]),head[0],getUniqueID(),head[2],head[3],encodedjson)
        for client1 in SmartServer().client_map.values():
            if client1.addr[0] not in videoService().videoservers_map:
                client1.SendData(data)
    
def handleStartorStopService(head, body, client):
    head = list(head)
    if body['status_code'] == 1:
        server_name = body['server_name']
        from VideoServer import videoService
        from SmartServer import SmartServer
        from handlers import getUniqueID
        encodedjson = json.dumps(body)
        head[3] = len(encodedjson)
        data = struct.pack('!4i{}s'.format(head[3]),head[0],getUniqueID(),head[2],head[3],encodedjson)
        videoserver = videoService().getVideoServer(server_name)
        if videoserver is not None:
            for client1 in SmartServer().client_map.values():
                if cmp(client1.addr[0],videoserver.getIp()) == 0:
                    client1.SendData(data)
#                     client.SendData(data)
        body['status_code'] = 2
        encodedjson = json.dumps(body)
        head[3] = len(encodedjson)
        data = struct.pack('!4i{}s'.format(head[3]),head[0],head[1],head[2],head[3],encodedjson)
        client.SendData(data)
    elif body['status_code'] == 2:
        print body
    
def handleIPCState(head, body, client):
    head = list(head)
    from VideoServer import videoService
    from SmartServer import SmartServer
    from handlers import getUniqueID
    server_name =  body['server_name']
    if body['status_code'] == 1:
        member = []
        for item in body['member']:
            ipc_state = videoService().getVideoIPCState(server_name, item['ipc_name'])
            item['ipc_state'] = ipc_state
            member.append(item)
        body['status_code'] = 2
        encodedjson = json.dumps(body)
        head[3] = len(encodedjson)
        data = struct.pack('!4i{}s'.format(head[3]),head[0],getUniqueID(),head[2],head[3],encodedjson)
        client.SendData(data)
    elif body['status_code'] == 2:
        print body
    elif body['status_code'] == 255:
        member = []
        for item in body['member']:
            videoService().setVideoIPCState(server_name, item['ipc_name'], item['ipc_state'])
            member.append(item)
        encodedjson = json.dumps(body)
        head[3] = len(encodedjson)
        data = struct.pack('!4i{}s'.format(head[3]),head[0],getUniqueID(),head[2],head[3],encodedjson)
        for client1 in SmartServer().client_map.values():
            if client1.addr[0] not in videoService().videoservers_map:
                client1.SendData(data)
         
protocolhandlers[1] = handleDeviceTypes
protocolhandlers[2] = handleSessionTypes
protocolhandlers[3] = handleUnits
protocolhandlers[4] = handleNodes
protocolhandlers[5] = handleSessions
protocolhandlers[6] = handleDevices
protocolhandlers[7] = handleDevArea
protocolhandlers[8] = handleSessionState
protocolhandlers[9] = handleDevDatas
protocolhandlers[10] = handleStartUpload
protocolhandlers[11] = handleDevTypeBaseDatas
protocolhandlers[12] = handleDataProperties
protocolhandlers[13] = handleControlSession
protocolhandlers[101] = handleVideoServers
protocolhandlers[102] = handleVideoIPCS
protocolhandlers[103] = handleVideoRecords
protocolhandlers[104] = handleVideoServiceState
protocolhandlers[105] = handleStartorStopService
protocolhandlers[106] = handleIPCState
        
