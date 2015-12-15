#coding=utf-8
#!/usr/bin/env python

'''
Created on 2015年3月4日

@author: sanhe
'''

from Queue import Queue
import time
import multiprocessing
# from checkError import PumpCheck
from threading import Timer
# import DataProcess
import torndb

class SmartServer(object):
    '''
    classdocs
    '''
    instance = None
    processList = []
    sessiondict = {}
    dataQueue = Queue()
    taskQueue = Queue()
    runFlag = True
    mysqlConnect_data =  torndb.Connection("127.0.0.1:3306", "mysql", user = "root", password = "123456")
    mysqlConnect_task =  torndb.Connection("127.0.0.1:3306", "mysql", user = "root", password = "123456")
    
    def __new__(cls, *args, **kwarg):
        if not cls.instance:
            cls.instance = super(SmartServer, cls).__new__(cls, *args, **kwarg)
        return cls.instance
        
    def addDataItem(self,dataitem):
        self.dataQueue.put(dataitem)
        
    def addSession(self,serial_name,session):
        self.sessiondict[serial_name] = session
        
    def getSession(self,serial_name):
        return self.sessiondict[serial_name]
        
    def addTask(self,starttime,task):
        self.taskQueue.put({'startTime' : starttime,'Task' : task})
        
#     def handleTaskQueue(self):
#         if self.runFlag:
#             task_timer = Timer(0.1,self.handleTaskQueue)
#     #         print "Enter handleTaskQueue_____________________"
#             task = None
#             try:
#                 task = self.taskQueue.get_nowait()
#             except Exception as e:
#                 print "handleTaskQueue Error: ", e
#             if task:
#                 if time.time() - task['startTime'] > 0.01 :
#                     task['Task'](self.mysqlConnect_task)
#                 else:
#                     self.taskQueue.put(task)
#             task_timer.start()
#          
#     def handleDataQueue(self):
#         if self.runFlag:
#             data_timer = Timer(0.1,self.handleDataQueue)
#     #         print "Enter HandleDataQueue____________________"
#             itemdata = None
#             try:
#                 itemdata = self.dataQueue.get_nowait()
#             except Exception as e:
#                 print "handleDataQueue Error: ", e
#             if itemdata:
#     #             print itemdata
#                 DataProcess.dataEntrance(itemdata,self.mysqlConnect_data)
#     #             self.addTask(time.time()+2, PumpCheck("1#","2#","3#"))
#             data_timer.start()
         
    def stop(self):
        for k in self.sessiondict:
            self.sessiondict[k].stop()
        self.runFlag = False
        self.mysqlConnect_data.close()
        self.mysqlConnect_task.close()
        
    def start(self):
        for k in self.sessiondict:
            self.processList.append(multiprocessing.Process(target=self.sessiondict[k]))
            
#         self.processList.append(multiprocessing.Process(target=self.handleDataQueue))
#         self.processList.append(multiprocessing.Process(target=self.handleTaskQueue))

        for p in self.processList:
            p.run()