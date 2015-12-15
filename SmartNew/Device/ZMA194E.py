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

device_Dict['ZMA194E'] = '三相电表'

class ZMA194E(device):

    def __init__(self):
        device.__init__(self)
        self._datadict = {
                          'DO1' : None,
                          'DO2' : None,
                          'DO3' : None,
                          'DO4' : None,
                          'DI1' : None,
                          'DI2' : None,
                          'DI3' : None,
                          'DI4' : None,
                          'RMSUA' : None,
                          'RMSUB' : None,
                          'RMSUC' : None,
                          'Udiff'  : None,
                          'RMSIA' : None,
                          'RMSIB' : None,
                          'RMSIC' : None,
                          'Idiff'  : None,
                          'Psum'  : None,
                          'Pfsum' : None,
                          'FreqA' : None,
                          'WH-1'  : None,
                          'DisCount' : None,
                    }
        
    @classmethod
    def genPratrolInstr(self, ID):
        arr = []
        crc = crc16()
        data = [ID,0x03,0x00,0x14,0x00,0x03]
        arr.append(crc.createarray(data))
        data = [ID,0x03,0x00,0x17,0x00,0x1A]
        arr.append(crc.createarray(data))
        data = [ID,0x03,0x00,0x3F,0x00,0x12]
        arr.append(crc.createarray(data))
        data = [ID,0x03,0x00,0x57,0x00,0x02]
        arr.append(crc.createarray(data))
#         data = [ID,0x06,0x00,0x16,0x00,0x02]
#         arr.append(crc.createarray(data))
        return arr
    
    @datalog
    def dataParse(self, data):
        import struct
        self._connect_Flag = True
        self.setDisConnect(0)
        try :
            data_type = data[2]//2
            if data_type == 3:
                self._setDataValue('DI4', (data[6] & 0x08) >> 3)
                self._setDataValue('DI3', (data[6] & 0x04) >> 2)
                self._setDataValue('DI2', (data[6] & 0x02) >> 1)
                self._setDataValue('DI1', data[6] & 0x01)
                self._setDataValue('DO4', (data[8] & 0x08) >> 3)
                self._setDataValue('DO3', (data[8] & 0x04) >> 2)
                self._setDataValue('DO2', (data[8] & 0x02) >> 1)
                self._setDataValue('DO1', data[8] & 0x01)
            elif data_type == 26:
                RMSUA = None
                RMSUB = None
                RMSUC = None
                RMSIA = None
                RMSIB = None
                RMSIC = None
                for i in range(13):
                    if i < 4 or 5 < i < 9 or i== 12: 
                        arr = data[3+i*4 : 7+i*4]
                        strdata = ''
                        for j in arr:
                            strdata = strdata + chr(j)
                        value = struct.unpack('!f',strdata)[0]
                        if i == 0:
                            RMSUA = value
                            self._setDataValue('RMSUA', value)
                        elif i == 1:
                            RMSUB = value
                            self._setDataValue('RMSUB', value)
                        elif i == 2:
                            RMSUC = value
                            self._setDataValue('RMSUC', value)
                        elif i == 6:
                            RMSIA = value
                            self._setDataValue('RMSIA', value)
                        elif i == 7:
                            RMSIB = value
                            self._setDataValue('RMSIB', value)
                        elif i == 8:
                            RMSIC = value
                            self._setDataValue('RMSIC', value)
                        elif i == 12:
                            self._setDataValue('Psum', value)
                import math                            
                Udiff = max(math.fabs(RMSUA - RMSUB), math.fabs(RMSUA - RMSUC), math.fabs(RMSUB - RMSUC))
                Idiff = max(math.fabs(RMSIA - RMSIB), math.fabs(RMSIA - RMSIC), math.fabs(RMSIB - RMSIC))
                self._setDataValue('Udiff', Udiff)
                self._setDataValue('Idiff', Idiff)
            elif data_type == 18:
                strdata = ''
                for j in data[3:7]:
                    strdata = strdata + chr(j)
                value = struct.unpack('!f',strdata)[0]
                self._setDataValue('Pfsum', value)
                strdata = ''
                for j in data[19:23]:
                    strdata = strdata + chr(j)
                value = struct.unpack('!f',strdata)[0]
                self._setDataValue('FreqA', value)
            elif data_type == 2:
                strdata = ''
                for j in data[3:7]:
                    strdata = strdata + chr(j)
                value = struct.unpack('!f',strdata)[0]
                self._setDataValue('WH-1', value)
        except Exception as e:
            print "PFP6G dataParse Error : ", e