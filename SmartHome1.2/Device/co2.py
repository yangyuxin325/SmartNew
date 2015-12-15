#coding=utf8
'''
Created on 2015年6月16日

@author: sanhe
'''

from crc_check import crc16
from aux_log import datalog
from device import device
from device import device_Dict

device_Dict['co2'] = 'co2探测器'

class co2(device):
    
    def __init__(self):
        device.__init__(self)
        self._datadict = {
                    'CO2' : None,
                    'DisCount' : None,
                    }
        
    @classmethod
    def genPratrolInstr(self, ID):
        data = [ID,0x04,0x00,0x00,0x00,0x01]
        crc = crc16()
        return [crc.createarray(data)]
    
    @datalog
    def dataParse(self, data):
        self._connect_Flag = True
        self.setDisConnect(0)
        try :
            CO2 = data[3]*256 + data[4]
            self._setDataValue('CO2', CO2)
        except Exception as e:
            print "co2 dataParse Error : ", e
            

             
