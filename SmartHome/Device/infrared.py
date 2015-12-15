#coding=utf8
'''
Created on 2015年6月16日

@author: sanhe
'''
import copy
import logging

logging.basicConfig(level = logging.DEBUG,
                    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt = '%d %b %Y %H:%M:%S',
                    filename = 'test.log',
                    filemode = 'w'
                    )

class infrared():
    
    SUPPORTED_INSTRUCTIONS = {
        "LED_AUTO"   : 0 ,
        "LED_ON"     : 1 ,
        "LED_OFF"    : 2 ,
        "LED_URGENT" : 3 ,
                         }
    
    def __init__(self):
        self._datadict = {
                    'YWren' : None,
                    'LedState' : None,
                    'DoorState' : None,
                    'InfoTime' : None,
                    'Temperature' : None,
                    'Humidity' : None,
                    'Lux' : None,
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
#         self._datadict.update({key : item})
        value = self._datadict[link_key]
        if value is not None :
            value.addExceptData(item)
            
    def addAverageDataItem(self, key, item, link_key, minute):
        if link_key not in self._datadict.keys() :
            return
#         self._datadict.update({key : item})
        value = self._datadict[link_key]
        if value is not None :
            value.addAverageData(key,item, minute)
            
    @classmethod
    def checkSum(self, array):
        check_sum = 0
        for data in array:
            check_sum += data
            check_sum &= 0xff
        array.append(check_sum)
        return array
        
    @classmethod
    def genPratrolInstr(self, ID):
        data = [0x99, ID, 0x00, 0xff, 0xff]
        return [self.checkSum(data)]
        
    @classmethod
    def genControlInstr(self, ID, instr):
        if instr not in self.SUPPORTED_INSTRUCTIONS.keys():
            err = "There is not a {} in infrared's SUPPORTED_INSTRUCTIONS".format(instr)
            raise Exception(err)
        data = [0x99, ID, 0x01, 0x00, self.SUPPORTED_INSTRUCTIONS[instr]]
        return self.checkSum(data)
    
    def dataParse(self, data):
        logging.info('infrared received data : %s' % str(data))
        self._connect_Flag = True
        self.setDisConnect(0)
        YWren = (data[3] & 3)
        LedState = ((data[3] & 12) >> 2)
        DoorState = (data[3] & 16) >> 4
#         device_state = (data[3] & 32) >> 5
        InfoTime = (data[4] * 15000 + data[5] * 70) // 1000
        Temperature = float(data[7]) + float(data[8]) / 100.0
        if 1 == data[6]:
            Temperature = -self.Temperature
        Humidity = float(data[9]) + float(data[10]) / 100.0
        Lux = data[14] * 256 + data[15]
        self._setDataValue('YWren', YWren)
        self._setDataValue('LedState', LedState)
        self._setDataValue('DoorState', DoorState)
        self._setDataValue('InfoTime', InfoTime)
        self._setDataValue('Temperature', Temperature)
        self._setDataValue('Humidity', Humidity)
        self._setDataValue('Lux', Lux)
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
            logging.error("infrared _setDataValue")
            
    def _getDataValue(self, dataname):
        if self._datadict[dataname] is not None :
            return self._datadict[dataname].DataValue
        else : 
            return False
        
    def DisConnected(self):
        return self._connect_Flag
    
