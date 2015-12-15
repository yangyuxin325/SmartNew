#coding=utf8
'''
Created on 2015年6月16日

@author: sanhe
'''

from aux_log import datalog
from device import device
from crc_check import crc16
from device import device_Dict

device_Dict['infrared'] = '红外探测器'

class infrared(device):
    
    SUPPORTED_INSTRUCTIONS = {
        "LED_AUTO"   : 0 ,
        "LED_ON"     : 1 ,
        "LED_OFF"    : 2 ,
        "LED_URGENT" : 3 ,
                         }
    
    def __init__(self):
        device.__init__(self)
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
    
#     @classmethod
#     def genPratrolInstr(self, ID):
#         data = [ID, 0x03, 0x00, 0x00, 0x00, 0x07]
#         crc = crc16()
#         return [crc.createarray(data)]
        
    @classmethod
    def genControlInstr(self, ID, instr):
        if instr not in self.SUPPORTED_INSTRUCTIONS.keys():
            err = "There is not a {} in infrared's SUPPORTED_INSTRUCTIONS".format(instr)
            raise Exception(err)
        data = [0x99, ID, 0x01, 0x00, self.SUPPORTED_INSTRUCTIONS[instr]]
        return self.checkSum(data)
    
    @datalog
    def dataParse(self, data):
        self._connect_Flag = True
        self.setDisConnect(0)
        try:
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
        except Exception as e:
            print "infrared dataParse Error : ", e
