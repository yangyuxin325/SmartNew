#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年12月14日

@author: sanhe
'''
from Device import *
import torndb
import threading
import time
import multiprocessing
from greenlet import greenlet
from Device.crc_check import crc16

def HexToString(array):
    snd = ''
    for i in array:
        snd += '%02x' % i
    return snd

device_dict = {
               'infrared' : infrared.infrared,
               'co2' : co2.co2,
               'stc_1' : mokuai.stc_1,
               'plc' : plc.plc,
               'sansu' : sansu.sansu,
               'triplecng' : triplecng.triplecng,
               'voc' : voc.voc,
               'wenkong' : wenkong.wenkong,
               'ZMA194E' : ZMA194E.ZMA194E,
               }

ename_constraintMap = {}

class deviceSet():
    def __init__(self, session_name, db):
        self._session_name = session_name
        self._id_devmap = {}
        self._cycleCmds = {}
        self._initData(db)
        
    def _initData(self,db):
        self._sqlConnection = torndb.Connection(db._addr, db._name, user = db._user, password = db._password)
        
        self._sqlConnection.close()
        
    def getCmdSet(self):
        cmdCount = 0
        line_cmdList = []
        for key,cmds in self._cycleCmd.items():
            for cmd in cmds :
                cmdCount += 1
                line_cmdList.append({"id" : cmdCount, "cmd" : HexToString(cmd), "dev_id" : key})
        return line_cmdList
    
    def ParseData(self,dev_id,data):
        if dev_id in self._id_devmap:
            self._id_devmap[dev_id].dataParse(data)
        else:
            strdata = ''
            for x in data:
                strdata = strdata + str(hex(x))
            msg = ("ParseData : %s ,found there is not device which it's dev_id = %d in Session %s") % strdata,
            dev_id, self._session_name
            print msg
            
class data_session():
    def __init__(self, name, port, interval, handleTask = None):
        self._name = name
        self._port = port
        self._interval = interval
        self._handleTask = handleTask
        self._device_set = deviceSet(self._name)
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
        self._alive = False