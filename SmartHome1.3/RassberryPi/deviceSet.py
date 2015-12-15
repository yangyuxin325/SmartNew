#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年6月26日

@author: sanhe
'''

from Device import *
import torndb
from Device.baseData import devBaseData,dataConstraint

def HexToString(array):
    snd = ''
    for i in array:
        snd += '%02x' % i
    return snd

class deviceSet():
    device_dict = {
               'infrared' : infrared.infrared,
               'co2' : co2.co2,
               'stc_1' : mokuai.stc_1,
               'plc' : plc.plc,
               'sansu' : sansu.sansu,
               'triplecng' : triplecng.triplecng,
               'voc' : voc.voc,
               'wenkong' : wenkong.wenkong,
               }
    
    def __init__(self,session_name):
        self._session_name = session_name
        self._dev_dict = {}
        self._devname_dict = {}
        self._devid_dict = {}
        self._cycleCmd = {}
        self._sqlConnection = torndb.Connection("127.0.0.1:3306", "smarthome", user = "root", password = "123456")
        self._initData()
        self._sqlConnection.close()

    def getDeviceSet(self):
        return self._dev_dict


    def getSessionName(self):
        return self._session_name
        
    def getCmdSet(self):
        cmdCount = 0
        line_cmdList = []
        for key,cmds in self._cycleCmd.items():
            for cmd in cmds :
                cmdCount += 1
                line_cmdList.append({"id" : cmdCount, "cmd" : HexToString(cmd), "dev_id" : key})
        return line_cmdList
    
    def getDeviceName(self, dev_id):
        if dev_id in self._devid_dict:
            return self._devid_dict[dev_id]
    
    def getDevice(self, dev_name):
        if dev_name in self._devname_dict:
            return self._dev_dict[self._devname_dict[dev_name]]
        else:
            return None
        
    def DisConnected(self,dev_id):
        if dev_id in self._dev_dict.keys():
            return self._dev_dict[dev_id].DisConnected()
        else :
            return None
        
    def setDisConnect(self, dev_id, value):
        if dev_id in self._dev_dict.keys():
            self._dev_dict[dev_id].setDisConnect(value)
#             print "SetDisConnect dev_id = " , dev_id
        
    def _initData(self):
#         sql = "select dev_name,dev_id,dev_type from devices where session_name = %s and dev_type = 'infrared'"
        sql = "select dev_name,dev_id,dev_type from devices where session_name = %s"
        devices = self._sqlConnection.query(sql, self._session_name)
        for device in devices :
            self._dev_dict[device['dev_id']] = self.device_dict[device['dev_type']]()
            self._devname_dict[device['dev_name']] = device['dev_id']
            self._devid_dict[device['dev_id']] = device['dev_name']
            self._cycleCmd.update({device['dev_id'] : self.device_dict[device['dev_type']].genPratrolInstr(device['dev_id'])})
#             print self._cycleCmd
            sql = 'select * from data_constraints where dev_name = %s and link_flag = 0'
            datas = self._sqlConnection.query(sql,device['dev_name'])
            for data in datas :
                constraint = dataConstraint(data['state'], data['min_variation'], data['min_val'],data['max_val'])
                dataitem = devBaseData(data['data_name'],constraint, 0, None)
                self._dev_dict[device['dev_id']].addDataItem(data['conf_name'],dataitem)
                if data["algorithm"] is not None :
                    self._dev_dict[device['dev_id']].addAlgorithm(data['conf_name'], data["algorithm"])
            sql = 'select * from data_constraints where dev_name = %s and link_flag = 1'
            datas = self._sqlConnection.query(sql,device['dev_name'])
            for data in datas :
                constraint = dataConstraint(data['state'], data['min_variation'], data['min_val'],data['max_val'])
                dataitem = devBaseData(data['data_name'],constraint, 0, None)
                if device['dev_type'] == 'plc' or device['dev_type'] == 'mokuai' :
                    sql =  'select link_key,link_type,link_para1 from data_links where conf_name = %s and dev_name = %s'
                    data_links = self._sqlConnection.query(sql,data['conf_name'],device['dev_name'])
                else :
                    sql = 'select link_key,link_type,link_para1 from conf_links where conf_name = %s'
                    data_links = self._sqlConnection.query(sql,data['conf_name'])
                    for data_link in data_links : 
                        if data_link['link_type'] == 'error' :
                            self._dev_dict[device['dev_id']].addExceptDataItem(data['conf_name'],dataitem,data_link['link_key'])
                        elif data_link['link_type'] == 'average' :
                            self._dev_dict[device['dev_id']].addAverageDataItem(data['conf_name'],dataitem,data_link['link_key'],data_link['link_para1'])
                
    
    def ParseData(self,dev_id,data):
        if dev_id in self._dev_dict.keys():
            self._dev_dict[dev_id].dataParse(data)
        else:
            print "there is not device which it dev_id = " , dev_id , " in Session ", self._session_name
        
devices = deviceSet("空调外机通道")
print devices.getCmdSet()
# 
# devices.ParseData(16,[16, 3, 2, 0, 0, 68, 71])

