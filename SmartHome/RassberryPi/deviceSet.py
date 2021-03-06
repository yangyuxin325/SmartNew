#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年6月26日

@author: sanhe
'''

from Device import infrared,co2,mokuai,plc,sansu,triplecng,voc,wenkong
import torndb
from Device.baseData import devBaseData,dataConstraint
import copy
import logging

# logging.basicConfig(level = logging.DEBUG,
#                     format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt = '%d %b %Y %H:%M:%S',
#                     filename = 'deviceSet.log',
#                     filemode = 'w'
#                     )

def HexToString(array):
    snd = ''
    for i in array:
        snd += '%02x' % i
    return snd

class deviceSet():
    device_dict = {
               'infrared' : infrared.infrared,
               'co2' : co2.co2,
               'mokuai' : mokuai.stc_1,
               'plc' : plc.plc,
               'sansu' : sansu.sansu,
               'triplecng' : triplecng.triplecng,
               'voc' : voc.voc,
               'wenkong' : wenkong.wenkong,
               }
    
    def __init__(self,session_name):
        self._session_name = session_name
        self._set = {}
        self._cycleCmd = []
        self._sqlConnection = torndb.Connection("127.0.0.1:3306", "smarthome", user = "root", password = "123456")
        self._initData()
#         for it in self._set :
#             print it
#         for it in self._cycleCmd:
#             print it
        
    def getCmdSet(self):
        return copy.deepcopy(self._cycleCmd)
        
    def _initData(self):
        sql = "select dev_name,dev_id,dev_type from devices where session_name = %s and dev_type = 'voc'"
        devices = self._sqlConnection.query(sql, self._session_name)
        for device in devices :
            self._set.update({device['dev_id'] : self.device_dict[device['dev_type']]()})
            self._cycleCmd.extend(self.device_dict[device['dev_type']].genPratrolInstr(device['dev_id']))
            print self._cycleCmd
            sql = 'select * from data_constraints where dev_name = %s'
            datas = self._sqlConnection.query(sql,device['dev_name'])
            for data in datas :
                constraint = dataConstraint(data['state'], data['min_variation'], data['min_val'],data['max_val'])
                dataitem = devBaseData(data['data_name'],constraint)
                if data['link_flag'] == 0 :
                    self._set[device['dev_id']].addDataItem(data['conf_name'],dataitem)
                else :
                    data_links = None
                    if device['dev_type'] == 'plc' or device['dev_type'] == 'mokuai' :
                        sql =  'select link_key,link_type,link_para1 from data_links where conf_name = %s and dev_name = %s'
                        data_links = self._sqlConnection.query(sql,data['conf_name'],device['dev_name'])
                    else :
                        sql = 'select link_key,link_type,link_para1 from conf_links where conf_name = %s'
                        data_links = self._sqlConnection.query(sql,data['conf_name'])
                    for data_link in data_links : 
                        if data_link['link_type'] == 'error' :
                            self._set[device['dev_id']].addExceptDataItem(data['data_name'],constraint,data_link['link_key'])
                        elif data_link['link_type'] == 'average' :
                            self._set[device['dev_id']].addAverageDataItem(data['data_name'],constraint,data_link['link_key'],data_link['link_para1'])
                
    
    def ParseData(self,dev_id,data):
        dataarr = []
        for i in range(len(data)) :
            dataarr.append(ord(data[i]))
        print dev_id, dataarr
#         logging.info('ParseData : %s' % str(dataarr))
        self._set[dev_id].dataParse(dataarr)
    
    

