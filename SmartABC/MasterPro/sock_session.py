#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年12月4日

@author: sanhe
'''

from SmartServer import AsyncClient
from SmartServer import Connection
from data_session import data_session
import multiprocessing
import time
import threading

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

class sock_sessionA(AsyncClient):
    def __init__(self, para, sock=None, handleData=None, session_map=None):
        self._para = para
        if self._sock is not None:
            AsyncClient.__init__(self, self._sock, handleData, session_map)
        self.process_map = {}
        self.channel_map = {}
        self.dataSession_map = {}
        self._data_dict = {}
        self._data_cache = {}
        self._state = False
        
    def initData(self,name,ip):
        if self._sock or self._type is 2:
            self._state = True
#         数据初始化，状态为断线的数据标记都为false
    
    def start(self,handleCycleData):
        for channel in self.dataSession_map:
            session = self.dataSession_map[channel]
            p = multiprocessing.Process(target=session)
            self.process_map[channel] = p
            p.start()
            th = MyThread(session)
            self.thread_map[channel] = th
            th.start()
                
    def putTask(self, channel, data):
        if channel in self.dataSession_map:
            if self.dataSession_map[channel].State():
                self.dataSession_map[channel].putTaskQueue(data)
            return True
        return False
    
class sock_sessionB(Connection):
    def __init__(self, Stype, handleData=None, session_map=None):
        self._type = Stype   #type 4 本身区域 5 单元  6本身节点
        self._session_dict = {}
        self._data_dict = {}
        self._data_cache = {}
        self._disflag = False