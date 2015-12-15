#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年7月21日

@author: sanhe
'''

def HexToString(array):
    snd = ''
    for i in array:
        snd += '%02x' % i
    return snd

# data = [0x15,0x06,0x00,0x0d,0x00,0x01]
# crc = crc16()
# arr = crc.createarray(data)
# print arr
# da dd

from serial import Serial
com = Serial('/dev/ttyUSB0',9600)
import voc
import co2
import infrared
import sansu
import ZMA194E
import plc
import mokuai
import PFP6G
# # com.open()
import time
# 3DA031B4

data = [0x0D,0x03,0x00,0x23,0x00,0x24]
from crc_check import crc16
senddata = crc16().createarray(data)

# import struct
# print "电流值 :", struct.unpack("f",'\x17\x6f\xc3\xda')[0]
# 
# 
# print bin(400)

# IA = DOUBLE('07c207c9',2)
# print "电流值： ", IA

while True :
# for arr in  plc.genPratrolInstr(1):
#     cmd = HexToString(arr)
#     print cmd
    for arr in  PFP6G.PFP6G.genPratrolInstr(8):
#     for arr in  sansu.sansu.genPratrolInstr(3):
        cmd = HexToString(arr)
        print cmd
        com.write(cmd.decode('hex'))
        flag = True
        data = ""
        count = 0
        while flag:
            time.sleep(0.01)
            count = count + 1
            n = com.inWaiting()
            flag1 = False
#             print "START"
            if n > 0:
                if flag1 is True:
                    flag1 = False
#                     print "SECOND"
                else:
                    flag1 = True
#                     print "FIRST"
                subdata = com.read(n)
#                 print "SUB : ", subdata.encode("hex")
                data = data + subdata
                if flag1 is True:
                    continue
#                     print "END"
            else:
                flag1 = False
            if (cmp(data,"") != 0 and n == 0) or count == 50:
                flag = False
                strdata = data.encode("hex")
                print "RECEIVED : ", strdata,"COUNT : ", count
                data = ""
                count = 0