#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年7月8日

@author: sanhe
'''
from baseData import devBaseData,dataConstraint
from infrared import infrared

infrared1 = infrared()
print  isinstance(22,infrared)

YwrenConstriant = dataConstraint(1,1.0, None, None)
Ywren = devBaseData('101有无人',YwrenConstriant)
infrared1.addDataItem('YWren',Ywren)

LedStateConstriant = dataConstraint(1,1.0, None, None)
LedState = devBaseData('101 Led灯状态',LedStateConstriant)
infrared1.addDataItem('LedState',LedState)

DoorStateConstriant = dataConstraint(1,1.0, None, None)
DoorState = devBaseData('101门磁',DoorStateConstriant)
infrared1.addDataItem('DoorState',DoorState)

InfoTimeConstriant = dataConstraint(1,10.0, None, None)
InfoTime = devBaseData('101无感应时间',InfoTimeConstriant)
infrared1.addDataItem('InfoTime',InfoTime)

TemperatureConstriant = dataConstraint(1,0.5,-50.0,50.0)
Temperature = devBaseData('101红外温度',TemperatureConstriant)
infrared1.addDataItem('Temperature',Temperature)
tempError = devBaseData('101红外温度异常',dataConstraint(1,1.0, None, None))
infrared1.addExceptDataItem('tempError',tempError,'Temperature')
temp1M = devBaseData('101红外温度1分钟平均',dataConstraint(1,0.2, None, None))
infrared1.addAverageDataItem('temp1M',temp1M,'Temperature',1)
temp5M = devBaseData('101红外温度5分钟平均',dataConstraint(1,0.2, None, None))
infrared1.addAverageDataItem('temp5M',temp5M,'Temperature',5)

HumidityConstraint = dataConstraint(1,1.0,1.0,99.0)
Humidity = devBaseData('101红外湿度',HumidityConstraint)
infrared1.addDataItem('Humidity',Humidity)
HumError = devBaseData('101红外湿度异常',dataConstraint(1,1.0, None, None))
infrared1.addExceptDataItem('HumError',HumError,'Humidity')

LuxConstraint = dataConstraint(1,1.0,None,None)
Lux = devBaseData('101光照度',LuxConstraint)
infrared1.addDataItem('Lux',Lux)

DisCountConstraint = dataConstraint(1,10.0,None,None)
DisCount = devBaseData('101红外通信故障',DisCountConstraint)
infrared1.addDataItem('DisCount',DisCount)

# infrared1.dataParse([153, 21, 0, 2, 12, 45, 0, 22, 78, 56, 67, 3, 4, 100, 0, 86, 137])
# print infrared1.getDataValue("Temperature")
# print infrared1.getDataValue("tempError")

from co2 import co2
co2_1 = co2()

CO2Constraint = dataConstraint(1,2.0,1.0,5000.0)
CO2 = devBaseData('110CO2值',CO2Constraint)
co2_1.addDataItem('CO2',CO2)
CO2Error = devBaseData('110CO2值异常',dataConstraint(1,1.0, None, None))
co2_1.addExceptDataItem('CO2Error',CO2Error,'CO2')

DisCountConstraint = dataConstraint(1,10.0,None,None)
DisCount = devBaseData('110CO2通信故障',DisCountConstraint)
co2_1.addDataItem('DisCount',DisCount)

# co2_1.dataParse([33, 4, 2, 1, 237, 249, 42])
# print co2_1.getDataValue("CO2")
# print co2_1.getDataValue("CO2Error")

from mokuai import stc_1
stc_1_first = stc_1()

DOConstriant = dataConstraint(1,1.0,None,None)

DO1 = devBaseData('主风柜排风机低速/高速',DOConstriant)
stc_1_first.addDataItem('DO1', DO1)

DO2 = devBaseData('主风柜排风机停止/开启',DOConstriant)
stc_1_first.addDataItem('DO2', DO2)

DO3 = devBaseData('闷顶排风机低速/高速',DOConstriant)
stc_1_first.addDataItem('DO3', DO3)

DO4 = devBaseData('闷顶排风机停止/开启',DOConstriant)
stc_1_first.addDataItem('DO4', DO4)

DO5 = devBaseData('地下室送\排风机低速/高速',DOConstriant)
stc_1_first.addDataItem('DO5', DO5)

DO6 = devBaseData('地下室送\排风机停止/开启',DOConstriant)
stc_1_first.addDataItem('DO6', DO6)

DO7 = devBaseData('室内风盘冷水侧开关阀',DOConstriant)
stc_1_first.addDataItem('DO7', DO7)

DO8 = devBaseData('室内风盘热水侧开关阀',DOConstriant)
stc_1_first.addDataItem('DO8', DO8)

DIConstriant = dataConstraint(1,1.0,None,None)

DI1 = devBaseData('室内风盘热供水侧V1开到位反馈',DIConstriant)
stc_1_first.addDataItem('DI1', DI1)

DI2 = devBaseData('室内风盘热供水侧V1关到位反馈',DIConstriant)
stc_1_first.addDataItem('DI2', DI2)

DI3 = devBaseData('室内风盘热回水侧V2开到位反馈',DIConstriant)
stc_1_first.addDataItem('DI3', DI3)

DI4 = devBaseData('室内风盘热回水侧V2关到位反馈',DIConstriant)
stc_1_first.addDataItem('DI4', DI4)

DI5 = devBaseData('室内风盘冷供水侧V1开到位反馈',DIConstriant)
stc_1_first.addDataItem('DI5', DI5)

DI6 = devBaseData('室内风盘冷供水侧V1关到位反馈',DIConstriant)
stc_1_first.addDataItem('DI6', DI6)

DI7 = devBaseData('室内风盘冷回水侧V2开到位反馈',DIConstriant)
stc_1_first.addDataItem('DI7', DI7)

DI8 = devBaseData('室内风盘冷回水侧V2关到位反馈',DIConstriant)
stc_1_first.addDataItem('DI8', DI8)

AIConstriant1 = dataConstraint(1,0.3,-50.0,50.0)
AIConstriant2 = dataConstraint(1,0.3,1.0,99.0)
AIConstriant3 = dataConstraint(1,0.3,0.0,99.0)

AI1 = devBaseData('主风柜出风温度',AIConstriant1)
stc_1_first.addDataItem('AI1', AI1)
AI1Error = devBaseData('主风柜出风温度异常',dataConstraint(1,1.0, None, None))
stc_1_first.addExceptDataItem('AI1Error',AI1Error,'AI1')

AI2 = devBaseData('主风柜出风湿度',AIConstriant2)
stc_1_first.addDataItem('AI2', AI2)
AI2Error = devBaseData('主风柜出风湿度异常',dataConstraint(1,1.0, None, None))
stc_1_first.addExceptDataItem('AI2Error',AI2Error,'AI2')

AI3 = devBaseData('主风柜回风温度',AIConstriant1)
stc_1_first.addDataItem('AI3', AI3)
AI3Error = devBaseData('主风柜回风温度异常',dataConstraint(1,1.0, None, None))
stc_1_first.addExceptDataItem('AI3Error',AI3Error,'AI3')

AI4 = devBaseData('主风柜回风湿度',AIConstriant2)
stc_1_first.addDataItem('AI4', AI4)
AI4Error = devBaseData('主风柜回风湿度异常',dataConstraint(1,1.0, None, None))
stc_1_first.addExceptDataItem('AI4Error',AI4Error,'AI4')

AI5 = devBaseData('主风柜新风温度',AIConstriant1)
stc_1_first.addDataItem('AI5', AI5)
AI5Error = devBaseData('主风柜新风温度异常',dataConstraint(1,1.0, None, None))
stc_1_first.addExceptDataItem('AI5Error',AI5Error,'AI5')

AI6 = devBaseData('主风柜新风湿度',AIConstriant2)
stc_1_first.addDataItem('AI6', AI6)
AI6Error = devBaseData('主风柜新风湿度异常',dataConstraint(1,1.0, None, None))
stc_1_first.addExceptDataItem('AI6Error',AI6Error,'AI6')

AI7 = devBaseData('一层地板温度探头',AIConstriant1)
stc_1_first.addDataItem('AI7', AI7)
AI7Error = devBaseData('一层地板温度探头异常',dataConstraint(1,1.0, None, None))
stc_1_first.addExceptDataItem('AI7Error',AI7Error,'AI7')

AI8 = devBaseData('主风柜配电柜内温度探头',AIConstriant3)
stc_1_first.addDataItem('AI8', AI8)
AI8Error = devBaseData('主风柜配电柜内温度探头异常',dataConstraint(1,1.0, None, None))
stc_1_first.addExceptDataItem('AI8Error',AI8Error,'AI8')

DisCountConstraint = dataConstraint(1,10.0,None,None)
DisCount = devBaseData('主配电柜STC-1通信故障',DisCountConstraint)
stc_1_first.addDataItem('DisCount',DisCount)

# stc_1_first.dataParse([15, 4, 16, 4, 214, 6, 68, 5, 23, 6, 60, 4, 224, 6, 1, 6, 47, 2, 253, 18, 135])
# print stc_1_first.getDataValue("AI8")
# print stc_1_first.getDataValue("AI8Error")
# stc_1_first.dataParse([15, 1, 1, 224, 82, 232])
# stc_1_first.dataParse([15, 2, 1, 33, 99, 120])

from sansu import sansu
sansu1 = sansu()

Wind = devBaseData('101三速风机风速',dataConstraint(1,1.0, None, None))
sansu1.addDataItem('Wind',Wind)

Fa1 = devBaseData('101三速风机阀门1',dataConstraint(1,1.0, None, None))
sansu1.addDataItem('Fa1',Fa1)

Fa2 = devBaseData('101三速风机阀门2',dataConstraint(1,1.0, None, None))
sansu1.addDataItem('Fa2',Fa2)

DisCountConstraint = dataConstraint(1,5.0,None,None)
DisCount = devBaseData('101三速风机通信故障',DisCountConstraint)
sansu1.addDataItem('DisCount',DisCount)

# sansu1.dataParse([1, 3, 6, 0, 0, 0, 0, 0, 0, 33, 117])
# print sansu1.getDataValue("Wind")

from voc import voc
voc1 = voc()

VOC = devBaseData('110VOC值',dataConstraint(1,0.5, None, None))
voc1.addDataItem('VOC', VOC)
VOCError = devBaseData('110VOC值异常',dataConstraint(1,1.0, None, None))
voc1.addExceptDataItem('VOCError', VOCError, 'VOC')

Temperature = devBaseData('110VOC温度',dataConstraint(1,0.5, None, None))
voc1.addDataItem('Temperature', Temperature)

Humidity = devBaseData('110VOC湿度',dataConstraint(1,0.5, None, None))
voc1.addDataItem('Humidity', Humidity)

DisCountConstraint = dataConstraint(1,10.0,None,None)
DisCount = devBaseData('110VOC通信故障',DisCountConstraint)
voc1.addDataItem('DisCount',DisCount)

# voc1.dataParse([34, 4, 12, 0, 0, 1, 4, 0, 49, 0, 0, 0, 0, 0, 0, 181, 104])
# print voc1.getDataValue("Temperature")
# print voc1.getDataValue("VOCError")

from wenkong import wenkong
wenkong1 = wenkong()

OnOff = devBaseData('101温控器开关机',dataConstraint(1,1.0, None, None))
wenkong1.addDataItem('OnOff', OnOff)

Mode = devBaseData('101温控器模式',dataConstraint(1,1.0, None, None))
wenkong1.addDataItem('Mode', Mode)

SetTemp = devBaseData('101温控器设定温度',dataConstraint(1,1.0, None, None))
wenkong1.addDataItem('SetTemp', SetTemp)

Wind = devBaseData('101温控器风速',dataConstraint(1,1.0, None, None))
wenkong1.addDataItem('Wind', Wind)

Temperature = devBaseData('101温控器温度',dataConstraint(1,1.0, None, None))
wenkong1.addDataItem('Temperature', Temperature)

DisCountConstraint = dataConstraint(1,10.0,None,None)
DisCount = devBaseData('101温控器通信故障',DisCountConstraint)
wenkong1.addDataItem('DisCount',DisCount)

wenkong1.dataParse([32, 3, 16, 0, 0, 0, 2, 20, 0, 0, 3, 0, 0, 0, 0, 0, 0, 22, 0, 127, 128])
print wenkong1.getDataValue("Temperature")