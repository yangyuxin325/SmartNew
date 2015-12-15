#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年8月6日

@author: sanhe
'''
from data_session import data_session
import handlers
import asyncore
import socket
import multiprocessing
import time
import threading
from sock_session import sock_sessionA
from sock_session import sock_sessionB
from MasterPro.DB_Para import DB_Para

class Connection():
    pass


class AsyncClient(asyncore.dispatcher):
    def __init__(self, sock, handleData = None, client_map = None):
        asyncore.dispatcher.__init__(self, sock)
        self._handleData = handleData
        self._client_map = client_map
        self._start_tell = False
        self.buffer = ''
        self._lock = threading.Lock()
        self._keepAlive = True
        import struct
        self._heartData = struct.pack('!4i', 0, 0, 0, 0)
        self._keepTimer = threading.Timer(1,self.handle_timer)
#         self.StartHeartBeat()
        
    def StartHeartBeat(self):
        if self._keepAlive :
            print "StartHeartBeat : "
            if self.connected:
                self._keepTimer = threading.Timer(1,self.handle_timer)
                self._keepTimer.start()
        
    def handle_timer(self):
        self._keepAlive = True
        self.send(self._heartData)
        print "handle_timer : "
        self.StartHeartBeat()
        
    def handle_read(self):
#         print "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR"
        self._keepAlive = False
        self._keepTimer.cancel()
        if self._handleData is not None:
            self._handleData(self)
            
    def SendData(self, data):
        if self.connected is False :
            return
        self._keepAlive = False
        self._keepTimer.cancel()
        self.buffer = data
        sent = self.send(self.buffer)
#         print "has Send : SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSss" , sent
        if len(self.buffer) > sent:
            time.sleep(0.1)
            self.SendData(self.buffer[sent:])
            print "SendData : ", self.buffer
        self.StartHeartBeat()
        
        
    def handle_close(self):
        print self.addr , "is Closed !"
#         asyncore.dispatcher.handle_close(self)
        try :
            if self._client_map is not None :
                if id(self) in self._client_map :
                    del self._client_map[id(self)]
            handlers.handleClientClosed(self.addr[0])
        except Exception as e:
            print "handle_close Got Error : ", e
        self.close()
#         self.StartHeartBeat()
                
    def tellFlag(self):
        return self._start_tell
                
    def Start_tell(self):
        self._start_tell = True
            
class AsyncServer(asyncore.dispatcher):
    def __init__(self, host, port, handleConnect = None):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self._handleConnect = handleConnect
          
    def handle_accept(self):
        asyncore.dispatcher.handle_accept(self)
        pair = self.accept()
        if pair is not None :
            sock, addr = pair
            print "%s connected" % repr(addr)
            if self._handleConnect is not None :
                self._handleConnect(sock)
            
    def run(self):
        self.listen(5)
    
class MyThread(threading.Thread):
    def __init__(self, session):
        threading.Thread.__init__(self)
        self._session = session
        self._stop_thread = False
        
    def run(self):
        while not self._stop_thread :
#             print "start _doResult :", id(self._session)
            task = self._session.getResultQueue()
            if task :
                if task['handle'] :
                    task['handle'](task['data'])
#                 for client in SmartServer().client_map.values():
#                     client.send("Hello{}\n".format(id(self._session)))
            time.sleep(0.01)
            
    def stop(self):
        self._stop_thread = True
            

class SmartServer(object):
    instance = None
    logic_map = {}
    db_mysql = DB_Para("127.0.0.1:3306", "smarthome", "root", "123456")
    unitcmp_logiclist = {}
    unitctrl_logiclist = {}
    areacmp_logiclist = {}
    areactrl_logiclist = {}
    ip_ServerPara = {}
    name_sessServer = {}
    name_sockSesssion = {}
    sockSess_name = {}
    nodeunit_map = {}
    pre_Name = None
    
    channel_map = {
#                     u'空调外机通道' : '/dev/ttyUSB1',
                    u"二层室内设备通道" : '/dev/ttyUSB0',
#                     u"一层室内设备通道" : '/dev/ttyUSB3',
#                     u"地下室I/O模块通道" : '/dev/ttyUSB0',
                   }
    server_dict = {
                   'area_server' : 'area',
                   'unit_server' : 'unit',
                   'unit_node_serer' : 'unit_node',
                   }
    dataSession_map = {}
    process_map = {}
    client_map = {}
    Server = None
    thread_map = {}
    lastMsgNum = None
    area_connection = None
    
    def __new__(cls, *args, **kwarg):
        if not cls.instance:
            cls.instance = super(SmartServer, cls).__new__(cls, *args, **kwarg)
        return cls.instance
        
    def Init(self, Host, Port, handleConnect, channel_map = None):
        self._para = self.ip_ServerPara[Host]
        self._handleConnect = handleConnect
        self.workflag = False
        self.Server = AsyncServer(Host, Port, self._handleConnect)
        if channel_map is not None :
            self.__class__.channel_map = channel_map
        
    def stopAllChannels(self):
        Next_flag = False
        for channel,process in self.process_map.items():
            if  process.is_alive():
                Next_flag = True
                self.putTask(channel, {'MsgType' : 3, 'data' : {'state' : 0}})
            if channel in self.thread_map :
                if self.thread_map[channel].is_alive:
                    self.thread_map[channel].stop()
        if Next_flag:
            time.sleep(3)
            self.stopAllChannels()
        
    def channelStart(self, channel):
        try:
            if channel in self.process_map :
                print channel , self.process_map[channel].is_alive()
                if not self.dataSession_map[channel].State():
                    del self.process_map[channel]
                else :
                    self.putTask(channel,{'MsgType' : 3, 'data' : {'state' : 0}})
                    while self.dataSession_map[channel].State():
                        print channel, "is alive"
                        time.sleep(3)
                    del self.process_map[channel]
                if channel in self.thread_map :
                    if self.thread_map[channel].is_alive:
                        self.thread_map[channel].stop()
                    del self.thread_map[channel]
                    
        except Exception as e:
            print "channelStart Error : " , e
        if channel in self.channel_map :
            session = data_session(channel, self.channel_map[channel], 9600, 0.5, 
                                                    lambda self, data : handlers.MsgDict[data['MsgType']](self,data))
            self.dataSession_map[channel] = session
            if channel in self.dataSession_map:
                session = self.dataSession_map[channel]
                p = multiprocessing.Process(target=session)
                self.process_map[channel] = p
                p.start()
                th = MyThread(session)
                self.thread_map[channel] = th
                th.start()
            
    def startOldSession(self, channel):
        print "startOldSession : ", channel
        if channel in self.dataSession_map:
            del self.thread_map[channel]
            del self.process_map[channel]
            session = self.dataSession_map[channel]
            p = multiprocessing.Process(target=session)
            self.process_map[channel] = p
            p.start()
            th = MyThread(session)
            self.thread_map[channel] = th
            th.start()
            return True
        return False
            
    def Start(self):
        if self._para.Server_Type() == 'area':
            pass
        elif self.self._para.Server_Type() == 'unit':
            session = sock_sessionA(self.self._para)
            self.name_sockSesssion[self._para.Server_Name()] = session
            threading.Timer(5,self.unit_Start,id(session)) 
        elif self.self._para.Server_Type() == 'node':
            pass
        self.Server.run()
        threading.Thread(target=asyncore.loop).start()
#         session1 = midSession('172.16.1.13',9999)
#         session2 = midSession('172.16.1.13',8888)
#         asyncore.loop()

    def start_work(self):
        if self._para.Server_Type() == 'unit':
            self.server_dict
        self.workflag = True

    def unit_Start(self, session_id):
        flag = False
        area_session_id = None
        area_ip = None
        iplist = []
        for s_id, session in self.sockSession_map:
            if session.addr[0] in self.servertype_dict:
                if self.servertype_dict[session.addr[0]] == 'area':
                    flag = True
                    area_session_id = s_id
                    area_ip = session.addr[0]
                    self.sockSession_map[session_id].start(area_ip,self.ipserver_dict[area_ip])
                    iplist.append(self.Server.addr[0])
        if flag:
            for s_id, session in self.sockSession_map:
                if s_id != area_session_id and s_id != session_id:
                    self.sockSession_map[s_id].initData(area_ip,self.ipserver_dict[area_ip])
                    iplist.append(session.addr[0])
        else:
            for s_id, session in self.sockSession_map:
                self.sockSession_map[s_id].initData(self.Server.addr[0],self.ipserver_dict[self.Server.addr[0]])
                iplist.append(session.addr[0])
                
        for node,unit in self.nodeunit_map:
            if unit == self.ipserver_dict[self.Server.addr[0]]:
                if self.serverip_dict[node] not in iplist:
                    session = sock_sessionA(3)
                    self.sockSession_map[id(session)] = session
                    self.sockSession_map[id(session)].init_data(self.Server.addr[0])
        self.sockSession_map[session_id].start()
                
    def allChannelStart(self):
        for channel in self.channel_map.keys():
            self.channelStart(channel)
            
    def putTask(self, channel, data):
        if channel in self.dataSession_map:
            if self.dataSession_map[channel].State():
                self.dataSession_map[channel].putTaskQueue(data)
            return True
        return False
            
    def _doResult(self,session):
        while True :
            try :
                print "start _doResult :", id(session)
                task = session.getResultQueue()
                if task :
                    try :
                        if task['handle'] : 
                            task['handle'](task['data'])
                    except Exception as e:
                        print "_doResult got Error: ", e
                time.sleep(0.1)
            except Exception as e :
                print "_doResult : ", e

