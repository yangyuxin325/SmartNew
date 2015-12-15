#coding=utf8
'''
Created on 2015年6月16日

@author: sanhe
'''
from crc_check import crc16
from aux_log import datalog
from device import device
from device import device_Dict

device_Dict['plc'] = '可编程控制器'

class plc(device):
    
    SUPPORTED_INSTRUCTIONS = {
        'DO' : (1, 8),
        'DI' : (2, 12),
        'AO' : (3, 2),
        'AI' : (4, 8),
                }
    
    AI_CONVERT_DICT = {
                   1 : lambda x : (x - 4000) / 160.0,                 # /*plc温度：0——100*/
                   2 : lambda x : (x - 4000) / 160.0 - 50.0,          # /*plc温度：-50——50*/
                   3 : lambda x : (x - 4000) * 10.197 / 16000.0,      # /*plc压力：0——10.197*/
                   4 : lambda x : (x - 4000) * 8.0 / 1600.0 - 20.0,   # /*plc温度：-20——60*/
                   5 : lambda x : (x - 400) / 16.0,                   # /*温度：0——100*/
                   6 : lambda x : (x - 400) / 16.0 - 50.0,            # /*温度：-50——50*/
                   7 : lambda x : (x - 400) * 10.197 / 1600.0,        # /*压力：0——10.197*/
                   8 : lambda x : (x - 400) * 8.0 / 160.0 - 20.0,     # /*温度：-20——60*/
                   9 : lambda x : x/200.0                             # /*AO : 0-10v
                   }
    
    def __init__(self):
        device.__init__(self)
        self._datadict = {
                    'DisCount' : None,
                    }
        for key in self.SUPPORTED_INSTRUCTIONS.keys() :
            str_fisrt = key
            if self.SUPPORTED_INSTRUCTIONS[key][1] > 0 :
                for num in range(self.SUPPORTED_INSTRUCTIONS[key][1]):
                    str_name = str_fisrt + str(num+1)
                    self._datadict.update({str_name : None})
        self._Algorithm_dict = {}
        
        self._Parsedict = {
                           1 : self._D_IOParse,
                           2 : self._D_IOParse,
                           3 : self._AOparse,
                           4 : self._AIParse,
                           }
        
    def addAlgorithm(self, key, a_type):
        if a_type in self.AI_CONVERT_DICT.keys() : 
            self._Algorithm_dict.update({key : self.AI_CONVERT_DICT[a_type]})
        
    @classmethod
    def genPratrolInstr(self, ID):
        instr = []
        for key,val in self.SUPPORTED_INSTRUCTIONS.values():
            if val > 0 : 
                data = [ID,key,0x00,0x00,0x00,val]
                crc = crc16()
                instr.append(crc.createarray(data))
        import copy
        return copy.deepcopy(instr)
        
    @classmethod
    def genControlInstr(self, ID, instr, io_port ,val):
        if instr not in ('DO', 'AO'):
            err = "There is not a {} in plc's SUPPORTED_INSTRUCTIONS".format(instr)
            raise Exception(err)
        if io_port < 1 or io_port > self.SUPPORTED_INSTRUCTIONS[instr][1] : 
            err = "There is not a {} in plc's IO_PORT".format(instr)
            raise Exception(err)
        data = [ID,self.SUPPORTED_INSTRUCTIONS[instr][0],0x00,io_port,0x00,0x00]
        if instr == 'DO':
            if val == 1:
                data[4] = 0xff
        elif instr == 'AO':
            data[2] = (40001+io_port) >> 8
            data[3] = (40001+io_port) - data[2]*256
            data[4] = val >> 8
            data[5] = val & 0xff
        crc = crc16()
        return crc.createarray(data)
    
    def _D_IOParse(self, data):
        str_first = None
        if data[1] == 1:
            str_first = 'DO'
        elif data[1] == 2:
            str_first = 'DI'
        val = None
        for i in range(8*data[2]):
            if i < 8 :
                val = (data[3] & (1 << i)) >> i
            else:
                val = (data[4] & (1 << (i - 8))) >> (i - 8)
            str_name = str_first + str(i+1)
            self._setDataValue(str_name, val)
            
    def _AOparse(self, data):
        val1 = (data[3] << 8) + data[4]
        val2 = (data[5] << 8) + data[6]
        self._setDataValue('AO1', self._Algorithm_dict['AO1'](val1))
        self._setDataValue('AO2', self._Algorithm_dict['AO2'](val2))
        
    def _AIParse(self, data):
        str_first = 'AI'
        val = None
        for i in range(data[2]/2):
            val = (data[i*2+3] << 8) + data[i*2+4]
            str_name = str_first + str(i+1)
            if str_name in self._Algorithm_dict.keys():
                val = self._Algorithm_dict[str_name](val)
            self._setDataValue(str_name, val)
            
    @datalog  
    def dataParse(self, data):
        try :
            self._connect_Flag = True
            self.setDisConnect(0)
            self._Parsedict[data[1]](data)
        except Exception as e:
            print "plc dataParse :", e