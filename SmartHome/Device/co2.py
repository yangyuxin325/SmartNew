#coding=utf8
'''
Created on 2015年6月16日

@author: sanhe
'''
import copy
from crc_check import crc16
import logging

# logging.basicConfig(level = logging.DEBUG,
#                     format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt = '%d %b %Y %H:%M:%S',
#                     filename = 'co2.log',
#                     filemode = 'w'
#                     )
class co2():
    
    def __init__(self):
        self._datadict = {
                    'CO2' : None,
                    'DisCount' : None,
                    }
        self._connect_Flag = False
        
    def getDataDict(self):
        return copy.deepcopy(self._datadict)
        
    def addDataItem(self, key, item):
        if key not in self._datadict.keys() :
            return
        self._datadict.update({key : item})
        
    def addExceptDataItem(self, key, item, link_key):
        if link_key not in self._datadict.keys() :
            return
        self._datadict.update({key : item})
        value = self._datadict[link_key]
        if value is not None :
            value.addExceptData(value)
            
    def addAverageDataItem(self, key, item, link_key, minute):
        if link_key not in self._datadict.keys() :
            return
        self._datadict.update({key : item})
        value = self._datadict[link_key]
        if value is not None :
            value.addAverageData(value, minute)
        
    @classmethod
    def genPratrolInstr(self, ID):
        data = [ID,0x04,0x00,0x00,0x00,0x01]
        crc = crc16()
        return [crc.createarray(data)]
    
    def dataParse(self, data):
        logging.info('co2 received data : %s' % str(data))
        self._connect_Flag = True
        self.setDisConnect(0)
        CO2 = data[3]*256 + data[4]
        self._setDataValue('CO2', CO2)
        for key, value in self.getDataDict().items() : 
            logging.info("key : %s , value : %s" % (key, value))
            
    def setDisConnect(self, value):
        if value == 1 :
            if self._connect_Flag == False :
                self._disCount = self._disCount + value
        else:
            self.connect_Flag = False
            self._disCount = 0
        self._setDataValue('DisCount',self._disCount)
        
    def _setDataValue(self, dataname, value):
        try:
            if self._datadict[dataname] is not None :
                self._datadict[dataname].setValue(value)
        except:
            logging.error("co2 _setDataValue")
            
    def _getDataValue(self, dataname):
        if self._datadict[dataname] is not None :
            return self._datadict[dataname].DataValue
        else : 
            return False
    
