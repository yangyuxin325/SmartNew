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
#                     filename = 'wenkong.log',
#                     filemode = 'w'
#                     )

class wenkong():
    
    SUPPORTED_INSTRUCTIONS = {
        "OnOff"   : 2 ,
        "Mode"    : 3 ,
        "SetTemp" : 4 ,
        "Wind"    : 5 ,
                         }
    
    def __init__(self):
        self._datadict = {
                    'OnOff' : None,
                    'Mode' : None,
                    'SetTemp' : None,
                    'Wind' : None,
                    'Temperature' : None,
                    'DisCount' : None,
                    'Control_Mode' : None,
                    'Program_OnOff' : None,
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
        data = [ID,0x03,0x00,0x02,0x00,0x08]
        crc = crc16()
        return [crc.createarray(data)]
        
    @classmethod
    def genControlInstr(self, ID, instr, val):
        if instr not in self.SUPPORTED_INSTRUCTIONS.keys():
            err = "There is not a {} in wenkong's SUPPORTED_INSTRUCTIONS".format(instr)
            raise Exception(err)
        data = [ID, 0x06, 0x00, self.SUPPORTED_INSTRUCTIONS[instr], 0x00, val]
        crc = crc16()
        return crc.createarray(data)
    
    def dataParse(self, data):
        logging.info('wenkong received data : %s' % str(data))
        self._connect_Flag = True
        OnOff = data[4]
        Mode = data[5] * 256 + data[6]
        SetTemp = data[7] + data[8]/10.0
        Wind = data[9]*256 + data[10]
        Temp = data[17] + data[18]/10.0
        self._setDataValue('OnOff', OnOff)
        self._setDataValue('Mode', Mode)
        self._setDataValue('SetTemp', SetTemp)
        self._setDataValue('Wind', Wind)
        self._setDataValue('Temperature', Temp)
        p_onff = self._getDataValue('Program_OnOff')
        c_mode = self._getDataValue('Control_Mode')
        if p_onff and c_mode:
            if (p_onff & 1) == OnOff :
                self.setControlData('Control_Mode', 1)
            else:
                self.setControlData('Control_Mode', 0)
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
        if self._datadict[dataname] is not None :
            self._datadict[dataname].setValue(value)
            
    def _getDataValue(self, dataname):
        if self._datadict[dataname] is not None :
            return self._datadict[dataname].DataValue
        else : 
            return False
        
    def setControlData(self, dataname, value):
        if dataname not in ['Control_Mode','Program_OnOff']:
            err = "There is not a {} in wenkong's ControlData".format(dataname)
            raise Exception(err)
        self._setDataValue(self, dataname, value)
