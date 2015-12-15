#coding=utf8
'''
Created on 2015年6月16日

@author: sanhe
'''
from crc_check import crc16
from aux_log import datalog
from device import device
from device import device_Dict

device_Dict['sansu'] = '三速风机'

class sansu(device):
    
    SUPPORTED_INSTRUCTIONS = {
        "Wind"   : 0x64 ,
        "Fa1"    : 0x65 ,
        "Fa2"    : 0x66 ,
                         }
    
    def __init__(self):
        device.__init__(self)
        self._datadict = {
                    'Wind' : None,
                    'Fa1' : None,
                    'Fa2' : None,
                    'DisCount' : None,
                    }
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
    
    @datalog
    def dataParse(self, data):
        self._connect_Flag = True
        self.setDisConnect(0)
        try :
            Wind = data[3]*256 + data[4]
            Fa1 = data[5]*256 + data[6]
            Fa2 = data[7]*256 + data[8]
            self._setDataValue('Wind', Wind)
            self._setDataValue('Fa1', Fa1)
            self._setDataValue('Fa2', Fa2)
        except Exception as e:
            print "sansu dataParse Error : ", e