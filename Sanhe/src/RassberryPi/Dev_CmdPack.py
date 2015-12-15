#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年3月12日

@author: sanhe
'''
from crc_check import crc16

def checkSum(array):
    check_sum = 0
    for data in array:
        check_sum += data
        check_sum &= 0xff
    array.append(check_sum)
    return array
    
def HexToString(array):
    snd = ''
    for i in array:
        snd += '%02x' % i
    return snd

def plc_mokuaiCmdPack(ID, (PortType, portAmount)):
    data = [ID,PortType,0x00,0x00,0x00,portAmount]
    if PortType == 3 :
        data[3] = 42
    crc = crc16()
    return HexToString(crc.createarray(data))

def infraredCmdPack(ID,GN,RA,RV):
    data = [ID,GN,0x00,0x00,0x00,0x07]
    if GN == 6 :
        data[3] = RA
        data[5] = RV
    crc = crc16()
    return HexToString(crc.createarray(data))

def infraredCmdPack1(ID):
    data = [0x99,ID,0x00,0xff,0xff]
    return HexToString(checkSum(data))

def sansuCmdPack1(ID):
    data = [ID,0x03,0x00,0x64,0x00,0x03]
    crc = crc16()
    return HexToString(crc.createarray(data))

def wenkongCmdPack1(ID):
    data = [ID,0x07,0x81,0x00,0x01,0xff]
    crc = crc16()
    return HexToString(crc.createarray(data))

def co2CmdPack1(ID):
    data = [ID,0x04,0x00,0x00,0x00,0x01]
    crc = crc16()
    return HexToString(crc.createarray(data))

def vocCmdPack1(ID):
    data = [ID,0x04,0x00,0x00,0x00,0x06]
    crc = crc16()
    return HexToString(crc.createarray(data))

def tripleCgn(ID,type_id):
    data = [ID,0x03,0x00,0x00,0x00,type_id]
    addr = {5:44310,
            4:44320,
            7:44330,
            25:44340,
            1:44370,
            6:49001,
            16:28401,
            15:27901,
            2:28901}
    data[2] = addr.get(type_id)>>8;
    data[3] = addr.get(type_id)&0xff
    crc = crc16()
    return HexToString(crc.createarray(data))

CmdPackConfig = {
                 'plc' : plc_mokuaiCmdPack,
                 'mokuai' : plc_mokuaiCmdPack,
                 'infrared' : infraredCmdPack1,
                 'sansu' : sansuCmdPack1,
                 'wenkong' : wenkongCmdPack1,
                 'co2' : co2CmdPack1,
                 'voc' : vocCmdPack1,
                 'triplecgn' : tripleCgn
                 }

PackArrayConfig = {
                   'plc' : ((1,8),(2,12),(3,2),(4,8)),
                   'mokuai' : ((1,8),(2,12),(4,8)),
                   'triplecgn' : (1,2,4,5,6,7,15,16,25)
                   }