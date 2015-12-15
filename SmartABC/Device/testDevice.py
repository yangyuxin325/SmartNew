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

from PFP6G import PFP6G
pfp6g = PFP6G()
from baseData import devBaseData
from baseData import dataConstraint
DO1 = devBaseData('DO1',dataConstraint(1,1.0, None, None))
pfp6g.addDataItem('DO1', DO1)
DO2 = devBaseData('DO2',dataConstraint(1,1.0, None, None))
pfp6g.addDataItem('DO2', DO2)
DO3 = devBaseData('DO3',dataConstraint(1,1.0, None, None))
pfp6g.addDataItem('DO3', DO3)
DO4 = devBaseData('DO4',dataConstraint(1,1.0, None, None))
pfp6g.addDataItem('DO4', DO4)

DI1 = devBaseData('DI1',dataConstraint(1,1.0, None, None))
pfp6g.addDataItem('DI1', DI1)
DI2 = devBaseData('DI2',dataConstraint(1,1.0, None, None))
pfp6g.addDataItem('DI2', DI2)
DI3 = devBaseData('DI3',dataConstraint(1,1.0, None, None))
pfp6g.addDataItem('DI3', DI3)
DI4 = devBaseData('DI4',dataConstraint(1,1.0, None, None))
pfp6g.addDataItem('DI4', DI4)

RMSUA = devBaseData('A相电压',dataConstraint(1,1.0, None, None))
pfp6g.addDataItem('RMSUA', RMSUA)
RMSUB = devBaseData('B相电压',dataConstraint(1,1.0, None, None))
pfp6g.addDataItem('RMSUB', RMSUB)
RMSUC = devBaseData('C相电压',dataConstraint(1,1.0, None, None))
pfp6g.addDataItem('RMSUC', RMSUC)
Udiff = devBaseData('三相电压差',dataConstraint(1,1.0, None, None))
pfp6g.addDataItem('Udiff', Udiff)
RMSIA = devBaseData('A相电流',dataConstraint(1,1.0, None, None))
pfp6g.addDataItem('RMSIA', RMSIA)
RMSIB = devBaseData('B相电流',dataConstraint(1,1.0, None, None))
pfp6g.addDataItem('RMSIB', RMSIB)
RMSIC = devBaseData('C相电流',dataConstraint(1,1.0, None, None))
pfp6g.addDataItem('RMSIC', RMSIC)
Idiff = devBaseData('三相电流差',dataConstraint(1,1.0, None, None))
pfp6g.addDataItem('Idiff', Idiff)
Psum = devBaseData('合相有功功率',dataConstraint(1,1.0, None, None))
pfp6g.addDataItem('Psum', Psum)

Pfsum = devBaseData('合相功率因数',dataConstraint(1,1.0, None, None))
pfp6g.addDataItem('Pfsum', Pfsum)
FreqA = devBaseData('A相频率',dataConstraint(1,1.0, None, None))
pfp6g.addDataItem('FreqA', FreqA)

WH1 = devBaseData('正向有功一次侧',dataConstraint(1,1.0, None, None))
pfp6g.addDataItem('WH-1', WH1)

DisCountConstraint = dataConstraint(1,10.0,None,None)
DisCount = devBaseData('通信故障',DisCountConstraint)
pfp6g.addDataItem('DisCount',DisCount)

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
    for arr in  PFP6G.genPratrolInstr(13):
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
                listdata = []
                for i in range(0,len(strdata),2):
                    listdata.append(int(strdata[i:i+2],16))
                pfp6g.dataParse(listdata)
                print "RECEIVED : ", strdata,"COUNT : ", count
                data = ""
                count = 0
    for key, value in pfp6g.getDataDict().items():
        print key, value
