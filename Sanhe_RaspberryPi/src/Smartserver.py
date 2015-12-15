#coding=utf-8
#!/usr/bin/env python

'''
Created on 2015年2月5日

@author: sanhe
'''
import multiprocessing
from multiprocessing import Process
import sched, time
from Singleton import Singleton
from ReceiveSession import ReceiveSession

class SmartServer(Singleton):
    '''
    classdocs
    '''
    def __init__(self, data_dict, time_interval):
        '''
        Constructor
        '''
        self.__pList = []
        self.__data_dict = data_dict
        self.__fun_sched = sched.scheduler(time.time, time.sleep)
        self.__timer_interval = time_interval
        self.__lock = multiprocessing.Lock()
        self.__recv_data = None
        self.__session_dict = {}
    
    def addProcessData(self,itemData):
        self.__lock.acquire()
        self.__recv_data.append(itemData)
        self.__lock.release()
        
    def popProcessData(self):
        self.__lock.acquire()
        self.__recv_data.pop(0)
        self.__lock.release()
    
    def proc_func(self,port,baudrate,data_list):
        receiveSession = ReceiveSession(port,baudrate,data_list,self.__timer_interval)
        self.__session_dict[port] = receiveSession
        receiveSession.start()
        receiveSession.sendNext()
    
    def start(self):
        for (port,data) in self.__data_dict:
            p = Process(target=self.proc_func,args=(port,data["baudrate"],data["data_list"]))
            self.__pList.append(p)
        
        for p in self.__pList:
            p.start()
        for p in self.__pList:
            p.join()
        