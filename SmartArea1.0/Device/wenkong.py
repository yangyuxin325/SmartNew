#coding=utf8
'''
Created on 2015年6月16日

@author: sanhe
'''
from crc_check import crc16
from aux_log import datalog
from device import device
from device import device_Dict

device_Dict['wenkong'] = '温控器'

class wenkong(device):
    
    SUPPORTED_INSTRUCTIONS = {
        "OnOff"   : 2 ,
        "Mode"    : 3 ,
        "SetTemp" : 4 ,
        "Wind"    : 5 ,
                         }
    
    def __init__(self):
        device.__init__(self)
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
    
    @datalog
    def dataParse(self, data):
        self._connect_Flag = True
        self.setDisConnect(0)
        try :
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
            p_onff = self.getDataValue('Program_OnOff')
            c_mode = self.getDataValue('Control_Mode')
            if p_onff is not None and c_mode is not None:
                if (p_onff & 1) == OnOff :
                    self.setControlData('Control_Mode', 1)
                else:
                    self.setControlData('Control_Mode', 0)
        except Exception as e:
            print "wenkong dataParse Error : ", e
        
    def setControlData(self, dataname, value):
        if dataname not in ['Control_Mode','Program_OnOff']:
            err = "There is not a {} in wenkong's ControlData".format(dataname)
            raise Exception(err)
        self._setDataValue(self, dataname, value)