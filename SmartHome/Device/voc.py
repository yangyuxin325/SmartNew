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
#                     filename = 'voc.log',
#                     filemode = 'w'
#                     )

class voc():
    
    def __init__(self):
        self._datadict = {
                    'VOC' : None,
                    'Temperature' : None,
                    'Humidity' : None,
                    'DisCount' : None,
                    }
        self._connect_Flag = False
        self._disCount = 0
        
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
        data = [ID,0x04,0x00,0x00,0x00,0x06]
        crc = crc16()
        return [crc.createarray(data)]
    
    def dataParse(self, data):
        logging.info('voc received data : %s' % str(data))
        self._connect_Flag = True
        VOC = (data[3]*256 + data[4])/10.0
        Temperature = (data[5]*256 + data[6])/10.0
        Humidity = data[7]*256+data[8]
        self._setDataValue('VOC', VOC)
        self._setDataValue('Temperature', Temperature)
        self._setDataValue('Humidity', Humidity)
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
            logging.error("voc _setDataValue")
            
    def _getDataValue(self, dataname):
        if self._datadict[dataname] is not None :
            return self._datadict[dataname].DataValue
        else : 
            return False
    
