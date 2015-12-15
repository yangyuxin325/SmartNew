#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年2月5日

@author: sanhe
'''
from threading import Thread
from threading import Timer
from serial import Serial
from crc_check import crc16
from Smartserver import SmartServer
import datetime


class ReceiveSession(object):
    '''
    classdocs
    '''
    
    def __init__(self, port,baudrate,cycleList,interval):
        '''
        Constructor
        '''
        self.__port = port
        self.__baudrate = baudrate
        self.__com = None
        self.__alive = False
        self.__cmdList = []
        self.__cycleList = cycleList
        self.__interval = interval
        self.__timer = None
        self.__index = 0
        self.__starttime = datetime.datetime.now()
        
    def insert_cmd(self,item):
        self.__cmdList.append(item)
    
    def sendNext(self):
        self.__timer = Timer(self.interval,self.sendNext)
        cmd = None
        if len(self.__cmdList) > 0 :
            cmd = self.__cmdList.pop(0)
        elif len(self.__cycleList) > 0 :
                cmd = self.__cycleList.pop(self.__index)
                self.__index += 1
                self.__index = self.__index % (len(self.__cycleList) - 1)
        if cmd is not None :
            self.__com.write(cmd)
            self.__starttime = datetime.datetime.now()
            self.__timer.setDaemon(True)
            self.__timer.start()
        return cmd
    
    def stopTimer(self):
        self.__timer.cancel()
        
    def openSerial(self):
        try:
            self.__com = Serial(self.__port,self.__baudrate)
        except:
            self.__com = None
            print 'Open %s fail' % self.__port
            
    def closeSerial(self):
        if(type(self.com) != type(None)):
            self.__alive = False
            self.__com.close()
            self.__com = None
            return True
        return False
    
    def isOpen(self):
        return self.__com.isOpen()
        
    def start(self):
        if self.isOpen() :
            self.__alive = True
            th = Thread(target=self.__receiveThread)
            th.setDaemon(True)
            th.start()
            
    def stop(self):
        self.__alive = False
            
    def __processData(self,data):
        arr = [ord(x) for x in data]
        pos = 0
        total_len = len(arr)
        rest_data = None
        while(pos < total_len):
            item_len = arr[pos+1]
            if pos + item_len > total_len:
                rest_arr = arr[pos:]
                rest_data = [chr(x) for x in rest_arr]
                break;
            else:
                item_data = arr[pos:pos+item_len]
                if crc16().calcrc(item_data):
                    SmartServer().addProcessData((self.__port,item_data))
                else:
                    print "Received Error Data : ",item_data, "."
                pos = pos + item_len
        return rest_data
        
    def __receiveThread(self):
        data = ''
        while self.__alive:
            try:
                n = self.com.inWaiting()
                if n:
                    data = data + self.com.read(n)
#                     (datetime.datetime.now() - self.__starttime).seconds
                    data = self.__processData(data)
            except Exception as e:
                print 'receiveThread got an error: %s' % e
            