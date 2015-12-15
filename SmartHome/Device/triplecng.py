#coding=utf8
'''
Created on 2015年6月16日

@author: sanhe
'''
import copy
from crc_check import crc16
import logging

# logging.basicConfig(level = logging.DEBUG,
#                     format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt = '%d %b %Y %H:%M:%S',
#                     filename = 'triplecng.log',
#                     filemode = 'w'
#                     )

class triplecng():
    
    SUPPORTED_INSTRUCTIONS = {
        "OnOff"   :  (49001,0) ,
        "Mode"    :  (49002,0) ,
        "AC_Cool" :  (49003,1) ,
        "AC_Warm" :  (49004,1) ,
        "HotWater":  (49005,1) ,
        "AC_Diff" :  (44313,1) ,
        "WB_Diff" :  (44314,1) ,
                         }
    
    def __init__(self):
        self._datadict = {
                    '1_1' : None,
                    '2_1Error' : None,
                    '2_2Error' : None,
                    '2_3Error' : None,
                    '2_4Error' : None,
                    '2_5Error' : None,
                    '2_6Error' : None,
                    '2_7Error' : None,
                    '2_8Error' : None,
                    '2_9Error' : None,
                    '2_10Error' : None,
                    '2_11Error' : None,
                    '2_12Error' : None,
                    '2_13Error' : None,
                    '2_14Error' : None,
                    '2_15Error' : None,
                    '2_16Error' : None,
                    '2_17Error' : None,
                    '2_18Error' : None,
                    '2_19Error' : None,
                    '2_20Error' : None,
                    '2_21Error' : None,
                    '2_22Error' : None,
                    '2_23Error' : None,
                    '2_24Error' : None,
                    '2_25Error' : None,
                    '2_26Error' : None,
                    '2_27Error' : None,
                    '2_28Error' : None,
                    '2_29Error' : None,
                    '2_30Error' : None,
                    '2_31Error' : None,
                    '2_32Error' : None,
                    '4_1' : None,
                    '4_2' : None,
                    '4_3' : None,
                    '4_4' : None,
                    '5_1' : None,
                    '5_2' : None,
                    '5_3' : None,
                    '5_4' : None,
                    '5_5' : None,
                    '6_1' : None,
                    '6_2' : None,
                    '6_3' : None,
                    '6_4' : None,
                    '6_5' : None,
                    '7_1' : None,
                    '7_2' : None,
                    '7_3' : None,
                    '7_4' : None,
                    '7_5' : None,
                    '7_6' : None,
                    '15_1' : None,
                    '15_2' : None,
                    '15_3' : None,
                    '15_4' : None,
                    '15_5' : None,
                    '15_6' : None,
                    '15_7' : None,
                    '15_8' : None,
                    '15_9' : None,
                    '15_10' : None,
                    '15_11' : None,
                    '15_12' : None,
                    '15_13' : None,
                    '15_14' : None,
                    '15_15' : None,
                    '16_1' : None,
                    '16_2' : None,
                    '16_3' : None,
                    '16_4' : None,
                    '16_5' : None,
                    '16_6' : None,
                    '16_7' : None,
                    '16_8' : None,
                    '16_9' : None,
                    '16_10' : None,
                    '16_11' : None,
                    '16_12' : None,
                    '16_13' : None,
                    '16_14' : None,
                    '16_15' : None,
                    '16_16' : None,
                    '25_1' : None,
                    '25_2' : None,
                    '25_3' : None,
                    '25_4' : None,
                    '25_5' : None,
                    '25_6' : None,
                    '25_7' : None,
                    '25_8' : None,
                    '25_9' : None,
                    '25_10' : None,
                    '25_11' : None,
                    '25_12' : None,
                    '25_13' : None,
                    '25_14' : None,
                    '25_15' : None,
                    '25_16' : None,
                    '25_17' : None,
                    '25_18' : None,
                    '25_19' : None,
                    '25_20' : None,
                    '25_21' : None,
                    '25_22' : None,
                    '25_23' : None,
                    '25_24' : None,
                    '25_25' : None,
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
        instr = []
        addrs = {
            5:44310,
            4:44320,
            7:44330,
            25:44340,
            1:44370,
            6:49001,
            16:28401,
            15:27901,
            2:28901,
            }
        for addr in addrs.items():
            addr1 = addr[1] >> 8;
            addr2 = addr[1] & 0xff
            data = [ID,0x03,addr1,addr2,0x00,addr[0]]
            crc = crc16()
            instr.append(crc.createarray(data))
        return copy.deepcopy(instr)
        
        
    @classmethod
    def genControlInstr(self, ID, instr, val):
        if instr not in self.SUPPORTED_INSTRUCTIONS.keys():
            err = "There is not a {} in triplecng's SUPPORTED_INSTRUCTIONS".format(instr)
            raise Exception(err)
        Addr = self.SUPPORTED_INSTRUCTIONS[instr][0]
        valtype = self.SUPPORTED_INSTRUCTIONS[instr][1]
        val1 = None
        val2 = None
        if valtype != 1 : 
            val1 = val >> 8
            val2 = val - val1 * 256
        else : 
            val1 = (val * 10 + 65536) >> 8
            val2 = (val * 10 + 65536) & 0xff
        data = [ID, 0x10, Addr >> 8, Addr & 0xff, 0x00, 0x01, 0x02, val1, val2]
        crc = crc16()
        return [crc.createarray(data)]
    
    def dataParse(self, data):
        logging.info('triplecng received data : %s' % str(data))
#         self._connect_Flag = True
#         self.setDisConnect(0)
#         data_type = data[2]//2
#         str_type = str(type)
#         str_name = str_type + '_'
#         if data_type == 1 : 
#             str_name = str_name + str(1)
#             self._setDataValue(str_name, data[3] << 8 + data[4])
#         elif data_type == 2 :
#             for i in range(32) :
#                 str_name = str_name + str(i+1) + 'Error'
#                 if i < 8:
#                     self._setDataValue(str_name,(data[3] & (1 << i)) >> i) 
#                 elif i < 16:
#                     self._setDataValue(str_name,(data[4] & (1 << (i-8))) >> (i-8))
#                 elif i < 24:
#                     self._setDataValue(str_name,(data[5] & (1 << (i-16))) >> (i-16))
#                 else:
#                     self._setDataValue(str_name,(data[6] & (1 << (i-24))) >> (i-24))
#         elif data_type == 4 :
#             for i in range(4) :
#                 str_name = str_name + str(i+1)
#                 if i ==  1 :
#                     self._setDataValue(str_name,data[i*2+3] * 256 + data[i*2+4])
#                 else :
#                     if 0xff == data[i*2+3]:
#                         self._setDataValue(str_name,(data[i*2+3] << 8 + data[i*2+4] - 65536)//10)
#                     else:
#                         self._setDataValue('str_name',(data[i*2+3] << 8 + data[i*2+4])//10)
#         elif data_type == 5 :
#             for i in range(5) :
#                 str_name = str_name + str(i+1)
#                 self._setDataValue((data[i*2+3] * 256 + data[i*2+4])//10)
#         elif data_type == 6 :
#             for i in range(5) :
#                 str_name = str_name + str(i+1)
#                 if i ==  0 or i == 1 :
#                     self._setDataValue(str_name,data[i*2+3] * 256 + data[i*2+4])
#                 else :
#                     if 0xff == data[i*2+3]:
#                         self._setDataValue(str_name,(data[i*2+3] << 8 + data[i*2+4] - 65536)//10)
#                     else:
#                         self._setDataValue(str_name,(data[i*2+3] << 8 + data[i*2+4])//10)
#         elif data_type == 7 :
#             for i in range(6) :
#                 str_name = str_name + str(i+1)
#                 if i ==  0 or i == 2 or i == 4 :
#                     self._setDataValue(str_name,data[i*2+3] << 8 + data[i*2+4])
#                 else :
#                     if 0xff == data[i*2+3]:
#                         self._setDataValue(str_name,(data[i*2+3] << 8 + data[i*2+4] - 65536)//10)
#                     else:
#                         self._setDataValue(str_name,(data[i*2+3] << 8 + data[i*2+4])//10)
#         elif data_type == 15 : 
#             for i in range(15) :
#                 str_name = str_name + str(i+1)
#                 self._setDataValue(str_name,data[i*2+3] << 8 + data[i*2+4])
#         elif data_type == 16 : 
#             for i in range(16) :
#                 str_name = str_name + str(i+1)
#                 self._setDataValue(str_name,(data[i*2+3] << 8 + data[i*2+4])//10)
#         elif data_type == 25 : 
#             for i in range(25) :
#                 str_name = str_name + str(i+1)
#                 if 5<= i <= 6 or 9 == i or 13 == i or 17 == i or 24 == i:
#                     if 0xff == data[i*2+3]:
#                         self._setDataValue(str_name,(data[i*2+3] << 8 + data[i*2+4] - 65536)//10)
#                     else:
#                         self._setDataValue(str_name,(data[i*2+3] << 8 + data[i*2+4])//10)
#                 else:
#                     self._setDataValue(str_name,data[i*2+3] << 8 + data[i*2+4])
#         for key, value in self.getDataDict().items() : 
#             logging.info("key : %s , value : %s" % (key, value))
        
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
            logging.error("triplecng _setDataValue")
            
    def _getDataValue(self, dataname):
        if self._datadict[dataname] is not None :
            return self._datadict[dataname].DataValue
        else : 
            return False
    
