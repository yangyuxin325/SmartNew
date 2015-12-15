#coding=utf8
'''
Created on 2015年6月16日

@author: sanhe
'''
import copy
from crc_check import crc16

class sansu():
    
    SUPPORTED_INSTRUCTIONS = {
        "Wind"   : 0x64 ,
        "Fa1"    : 0x65 ,
        "Fa2"    : 0x66 ,
                         }
    
    def __init__(self):
        self._datadict = {
                    'Wind' : None,
                    'Fa1' : None,
                    'Fa2' : None,
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
        data = [ID,0x03,0x00,0x64,0x00,0x03]
        crc = crc16()
        return [crc.createarray(data)]
        
    @classmethod
    def genControlInstr(self, ID, instr, val):
        if instr not in self.SUPPORTED_INSTRUCTIONS.keys():
            err = "There is not a {} in sansu's SUPPORTED_INSTRUCTIONS".format(instr)
            raise Exception(err)
        data = [ID, 0x06, 0x00, self.SUPPORTED_INSTRUCTIONS[instr], 0x00, val]
        crc = crc16()
        return crc.createarray(data)
    
    def dataParse(self, data):
        self._connect_Flag = True
        self.setDisConnect(0)
        Wind = data[3]*256 + data[4]
        Fa1 = data[5]*256 + data[6]
        Fa2 = data[7]*256 + data[8]
        self._setDataValue('Wind', Wind)
        self._setDataValue('Fa1', Fa1)
        self._setDataValue('Fa2', Fa2)
        
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
    
