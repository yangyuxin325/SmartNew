#coding=utf8
'''
Created on 2015年6月16日

@author: sanhe
'''
from crc_check import crc16
from aux_log import datalog
from device import device
from device import device_Dict

device_Dict['voc'] = 'voc探测器'

class voc(device):
    
    def __init__(self):
        device.__init__(self)
        self._datadict = {
                    'VOC' : None,
                    'Temperature' : None,
                    'Humidity' : None,
                    'DisCount' : None,
                    }
        
    @classmethod
    def genPratrolInstr(self, ID):
        data = [ID,0x04,0x00,0x00,0x00,0x06]
        crc = crc16()
        return [crc.createarray(data)]
    
    @datalog
    def dataParse(self, data):
        self._connect_Flag = True
        self.setDisConnect(0)
        try:
            VOC = (data[3]*256 + data[4])/10.0
            Temperature = (data[5]*256 + data[6])/10.0
            Humidity = data[7]*256+data[8]
            self._setDataValue('VOC', VOC)
            self._setDataValue('Temperature', Temperature)
            self._setDataValue('Humidity', Humidity)
        except Exception as e:
            print "co2 dataParse Error : ", e