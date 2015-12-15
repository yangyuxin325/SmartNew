#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年8月3日

@author: sanhe
'''
import deviceSet
import threading
import time
import multiprocessing
from greenlet import greenlet
from Device.crc_check import crc16
import com_handlers

def Sum_Right(array):
    check_sum = 0
    for i in range(len(array) -1):
        check_sum += ord(array[i])
        check_sum &= 0xff
    if check_sum == ord(array[i+1]):
        return True
    else:
        return False

class data_session():
    def __init__(self, name, port, baudrate, interval, handleTask = None):
        self._name = name
        self._port = port
        self._baudrate = baudrate
        self._interval = interval
        self._device_set = deviceSet.deviceSet(name)
        import copy
        self._cycleList = copy.deepcopy(self._device_set.getCmdSet())
        self._cycleList.append({"id" : 0, "cmd" : "", "dev_id" : -1})
        self._ctrlCmdList = []
        self._ctrlCmdLock = threading.Lock()
        self._errorList = []
        self._errorStartTime = time.time()
        self._resultQueue = multiprocessing.Queue()
        self._taskQueue = multiprocessing.Queue()
        self._rlock = multiprocessing.Lock()
        self._tlock = multiprocessing.Lock()
        self._com = None
        self._handleTask = handleTask
        self._alive = False
        
    def State(self):
        return self._alive
    
    def setState(self, flag):
        self._alive = flag
        
    def getDeviceData(self):
        import copy
        return copy.deepcopy(self._device_set)
        
    @property
    def Name(self):
        return self._name

    def _CmdThread(self, cmd, delay_second):
        time.sleep(delay_second)
        self._ctrlCmdList.append(cmd)
    
    def AddSendCmd(self, cmd, delay_second):
        if delay_second > 0 :
            th = threading.Thread(target= self._CmdThread, args= (cmd, delay_second))
            th.start()
        else :
            self._ctrlCmdList.append(cmd)
        
    def getDevice(self, dev_name):
        return self._device_set.getDevice(dev_name)
        
#     def SetHandleTask(self, handle):
#         self._handleTask = handle
        
    def putResultQueue(self, handle, data):
        self._rlock.acquire()
        self._resultQueue.put_nowait({'handle' : handle, 'data' : data})
        self._rlock.release()
        
    def getResultQueue(self):
        result = None
        self._rlock.acquire()
        if not self._resultQueue.empty():
            result = self._resultQueue.get_nowait()
        self._rlock.release()
        if result:
            return result
        
    def putTaskQueue(self, data):
        self._tlock.acquire()
        self._taskQueue.put_nowait(data)
        self._tlock.release()
        
    def getTaskQueue(self):
        task = None
        self._tlock.acquire()
        if not self._taskQueue.empty():
            task = self._taskQueue.get_nowait()
        self._tlock.release()
        if task :
            return task
        
    def openSerial(self):
        try:
            import serial
            self._com = serial.Serial(self._port,self._baudrate)
        except:
            print 'Open %s , %s Serial fail' % (self._name, self._port)
            
    def isOpen(self):
        if self._com :
            return self._com.isOpen()
    
    def __call__(self):
        self.start()
            
    def start(self):
        if not self.isOpen() :
            self.openSerial()
        if self.isOpen() :
            self._alive = True
            #通道连接建立
#             import test
#             self.putResultQueue(test.hanldeSessionState, {'session_name' : self._name, 'session_state' : True})
            th = threading.Thread(target=self._doTask)
            th.start()
            com_handlers.doSessionState(self, 1)
            self._sendGR = greenlet(self._sendData)
            self._recvGR = greenlet(self._receiveData)
            self._sendGR.switch()
            
            
    def stop(self):
        import os
        print os.getpid(), self._name , "has stopped"
        self._alive = False
        com_handlers.doSessionState(self, 0)
            
    def closeSerial(self):
        if(type(self._com) != type(None)):
            self._alive = False
            print "closeSerial"
#             self._taskQueue.close()
            self._com.close()
            return True
        return False
    
    def _doTask(self):
        while self._alive:
            if self._taskQueue.empty() is False :
                print "Task Num : " , self._taskQueue.qsize()
                data = self._taskQueue.get_nowait()
                if self._handleTask is not None :
                    self._handleTask(self, data)
            time.sleep(0.01)

    def _sendData(self):
        self._cmd = None
        self._startTime = time.time()
        while self._alive :
            try:
                cmd = None
                data = ""
                if len(self._ctrlCmdList) > 0:
                    data = self._ctrlCmdList.pop(0)
                    print "指令队列添加 ：" ,data 
                else :
                    cmd = self._cycleList.pop(0)
#                     print "_sendData", self._cycleList
                    data = cmd["cmd"]
                self._cmd = cmd
#                 print data, "                 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX           _sendData"
                if data != "" :
                    self._com.write(data.decode('hex'))
                    self._sendTime = time.time()
                    self._recvGR.switch()
                else :
                    self._NoSendData(cmd)
            except Exception as e:
                print '_sendData got an error : %s' % e, self._name, self._port  
                self.closeSerial()
                #通道连接断开
#                 import test
#                 self.putResultQueue(test.hanldeSessionState, {'session_name' : self._name, 'session_state' : False})
                com_handlers.doSessionState(self, 0)
                self.start()
                
    def _receiveData(self):
        data = ''
#         readFlag = False
        self._read_interval = 0.01
        total =int(self._interval/self._read_interval)
        while self._alive :
            try:
                flag = True
                data = ""
                count = 0
                while flag:
                    time.sleep(self._read_interval)
                    count = count + 1
                    n = self._com.inWaiting()
                    flag1 = False
                    if n > 0:
                        if flag1 is True:
                            flag1 = False
                        else:
                            flag1 = True
                        subdata = self._com.read(n)
        #                 print "SUB : ", subdata.encode("hex")
                        data = data + subdata
                        if flag1 is True:
                            continue
                    else:
                        flag1 = False
                    if (cmp(data,"") != 0 and n == 0) or count == total:
                        flag = False
                        if count == total:
                            self._DisConnectProcess()
                        else:
                            self._dataProcess(data)
                self._sendGR.switch()
#             print "Start                 FFFFFXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX           _receiveData"
#             try :
#                 if readFlag is False:
#                     time.sleep(self._read_interval)
#                 n = self._com.inWaiting()
#                 if n :
#                     self._recvTime = time.time()
#                     data = self._com.read(n)
# #                     print "_receiveData : ", ord(data[0]),  "----------------", data
#                     self._dataProcess(data)
# #                     print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX           _receiveData"
#                     self._sendGR.switch()
#                 else :
#                     if readFlag is False :
#                         time.sleep(self._interval-self._read_interval)
#                         readFlag = True
#                     else :
#                         readFlag = False
#                         self._DisConnectProcess()
#                         self._sendGR.switch()
            except Exception as e:
                print '_receiveData got an error : %s' % e, self._name, self._port  
                self.closeSerial()
                #通道连接断开
#                 import test
#                 self.putResultQueue(test.hanldeSessionState, {'session_name' : self._name, 'session_state' : False})
                com_handlers.doSessionState(self, 0)
                self.start()
            
    def _NoSendData(self, cmd):
        if cmd is not None and cmd["dev_id"] == -1 :
            
#             print cmd,  self._device_set.getSessionName(),"Period is ", time.time() - self._startTime, "S ."
            
#             import DataProcess
#             DataProcess.dataProcess(self._device_set,self._resultQueue)
#             self._handleData()
            com_handlers.doDataProcess(self)
            periods = time.time() - self._startTime
            com_handlers.doFinishPeriod(self,periods)
            self._startTime = time.time()
            self._cycleList.append(self._cmd)
#             print "_NoSendData : ", self._cycleList
            if len(self._cycleList) == 1:
                time.sleep(10)
            if len(self._errorList) > 0:
                if time.time() - self._errorStartTime > 60 :
#                     print "断线指令添加： ", self._errorList
                    self._cycleList =  self._errorList + self._cycleList
                    self._errorList = []
                    self._errorStartTime = time.time()
                    
    def _dataProcess(self,data):
        strdata = data.encode("hex")
        listdata = []
        for i in range(0,len(strdata),2):
            listdata.append(int(strdata[i:i+2],16))
#         import os
#         print os.getpid(), "_dataProcess : ", listdata
        dev_id = 0
        if (ord(data[0]) == 0x99 and Sum_Right(data)) or crc16().calcrc(listdata):
            if (ord(data[0]) == 0x99) :
                dev_id = ord(data[1])
            else:
                dev_id = ord(data[0])
            #数据处理
            self._device_set.ParseData(dev_id,listdata)
#             for key,value in self._device_set.getDeviceSet()[dev_id].getDataDict().items():
#                 print '_dataProcess : ', key,value
#             import test
#             self._resultQueue.put_nowait({'handle' : test.doDataProcessing, 'data' : listdata})
            
#             self._handleData(listdata)
            if self._cmd is not None and self._cmd['dev_id'] == dev_id :
                self._cycleList.append(self._cmd)
                #设备上线
                if self._device_set.DisConnected(dev_id) :
                    self._device_set.setDisConnect(dev_id,0)
    
    def _DisConnectProcess(self):
        if self._cmd is not None:
#             print "无返回指令 ： ",self._cmd
            #设备断线
#             import test
#             self._resultQueue.put_nowait({'handle' : test.doSetDisCount, 'data' : self._cmd})
            self._device_set.setDisConnect(self._cmd["dev_id"],1)
            if self._device_set.DisConnected(self._cmd["dev_id"]) is False:
                self._errorList.append(self._cmd)
#                 print "断线指令 ： ",self._name, self._cmd
            else :
                self._cycleList.append(self._cmd)
#             self._cycleList.append(self._cmd)
        