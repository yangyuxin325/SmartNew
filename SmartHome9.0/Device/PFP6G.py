#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年9月11日

@author: sanhe
'''
from aux_log import datalog
from device import device
from crc_check import crc16
from device import device_Dict

device_Dict['PFP6G'] = '走水挂机'

class PFP6G(device):
    def __init__(self):
        device.__init__(self)
        self._datadict = {
                    'DisCount' : None,
                    }
    @classmethod
    def genPratrolInstr(self, ID):
        data = [ID,0x03,0x00,0x00,0x00,0x02]
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