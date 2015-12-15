#coding=utf8
'''
Created on 2015年6月18日

@author: sanhe
'''

from baseData import devBaseData,dataConstraint

from infrared import infrared

infrared1 = infrared()

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

HumidityConstraint = dataConstraint(1,1.0,None,None)
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

for key, value in infrared1.getDataDict().items() : 
    print key,value
    
    
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

for key, value in co2_1.getDataDict().items() : 
    print key,value
    
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

for key, value in stc_1_first.getDataDict().items() : 
    print key,value
    
for k in sorted(stc_1_first.getDataDict().keys()) :
    print k,stc_1_first.getDataDict()[k]
    
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

for key, value in sansu1.getDataDict().items() : 
    print key,value
    
from triplecng import triplecng
triplecng1 = triplecng()

data1_1 = devBaseData('温度补偿',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('1_1', data1_1)

data2_1 = devBaseData('空调回水感温故障',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_1', data2_1)

data2_2 = devBaseData('空调出水感温故障',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_2', data2_2)

data2_3 = devBaseData('水箱感温故障',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_3', data2_3)

data2_4 = devBaseData('环境感温故障',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_4', data2_4)

data2_5 = devBaseData('防冻1感温故障',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_5', data2_5)

data2_6 = devBaseData('防冻2感温故障',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_6', data2_6)

data2_7 = devBaseData('排气1感温故障',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_7', data2_7)

data2_8 = devBaseData('排气2感温故障',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_8', data2_8)

data2_9 = devBaseData('蒸发1A进温故障',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_9', data2_9)

data2_10 = devBaseData('蒸发1A出温故障',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_10', data2_10)

data2_11 = devBaseData('蒸发1B进温故障',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_11', data2_11)

data2_12 = devBaseData('蒸发1B出温故障',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_12', data2_12)

data2_13 = devBaseData('蒸发2A进温故障',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_13', data2_13)

data2_14 = devBaseData('蒸发2A出温故障',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_14', data2_14)

data2_15 = devBaseData('蒸发2B进温故障',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_15', data2_15)

data2_16 = devBaseData('蒸发2B出温故障',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_16', data2_16)

data2_17 = devBaseData('系统1高压保护',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_17', data2_17)

data2_18 = devBaseData('系统1低压保护',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_18', data2_18)

data2_19 = devBaseData('系统1防冻保护',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_19', data2_19)

data2_20 = devBaseData('系统2高压保护',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_20', data2_20)

data2_21 = devBaseData('系统2低压保护',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_21', data2_21)

data2_22 = devBaseData('系统2防冻保护',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_22', data2_22)

data2_23 = devBaseData('空调水流故障',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_23', data2_23)

data2_24 = devBaseData('相序保护',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_24', data2_24)

data2_25 = devBaseData('进出水温差过大保护',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_25', data2_25)

data2_26 = devBaseData('冬季防冻保护',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_26', data2_26)

data2_27 = devBaseData('系统1排气过高保护',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_27', data2_27)

data2_28 = devBaseData('系统2排气过高保护',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_28', data2_28)

data2_29 = devBaseData('过热保护',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_29', data2_9)

data2_30 = devBaseData('热源侧水流保护',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_30', data2_30)

data2_31 = devBaseData('空调模式防冻',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_31', data2_31)

data2_32 = devBaseData('系统其他保护（保留）',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('2_32', data2_32)

data4_1 = devBaseData('电热启动环温',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('4_1', data4_1)

data4_2 = devBaseData('电热启动延时',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('4_2', data4_2)

data4_3 = devBaseData('电热启动温度',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('4_3', data4_3)

data4_4 = devBaseData('电热启动回差',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('4_4', data4_4)

data5_1 = devBaseData('制冷设定',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('5_1', data5_1)

data5_2 = devBaseData('制热设定',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('5_2', data5_2)

data5_3 = devBaseData('水箱温度设定',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('5_3', data5_3)

data5_4 = devBaseData('空调回差设定',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('5_4', data5_4)

data5_5 = devBaseData('水箱回差设定',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('5_5', data5_5)

data6_1 = devBaseData('开关机',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('6_1', data6_1)

data6_2 = devBaseData('模式',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('6_2', data6_2)

data6_3 = devBaseData('制冷设定',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('6_3', data6_3)

data6_4 = devBaseData('制热设定',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('6_4', data6_4)

data6_5 = devBaseData('热水设定',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('6_5', data6_5)

data7_1 = devBaseData('除霜模式',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('7_1', data7_1)

data7_2 = devBaseData('进入温度',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('7_2', data7_2)

data7_3 = devBaseData('除霜周期',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('7_3', data7_3)

data7_4 = devBaseData('退出温度',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('7_4', data7_4)

data7_5 = devBaseData('除霜时间',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('7_5', data7_5)

data7_6 = devBaseData('除霜环境',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('7_6', data7_6)

data15_1 = devBaseData('压缩机1',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('15_1', data15_1)

data15_2 = devBaseData('压缩机2',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('15_2', data15_2)

data15_3 = devBaseData('四通阀A',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('15_3', data15_3)

data15_4 = devBaseData('四通阀B',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('15_4', data15_4)

data15_5 = devBaseData('补水阀',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('15_5', data15_5)

data15_6 = devBaseData('风机',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('15_6', data15_6)

data15_7 = devBaseData('循环水泵',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('15_7', data15_7)

data15_8 = devBaseData('热水水泵',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('15_8', data15_8)

data15_9 = devBaseData('空调电加热',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('15_9', data15_9)

data15_10 = devBaseData('热水电加热',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('15_10', data15_10)

data15_11 = devBaseData('报警',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('15_11', data15_11)

data15_12 = devBaseData('系统1电子膨胀阀A',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('15_12', data15_12)

data15_13 = devBaseData('系统1电子膨胀阀B',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('15_13', data15_13)

data15_14 = devBaseData('系统2电子膨胀阀A',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('15_14', data15_14)

data15_15 = devBaseData('系统2电子膨胀阀B',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('15_15', data15_15)

data16_1 = devBaseData('空调回水',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('16_1', data16_1)

data16_2 = devBaseData('空调出水',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('16_2', data16_2)

data16_3 = devBaseData('水箱',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('16_3', data16_3)

data16_4 = devBaseData('环境',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('16_4', data16_4)

data16_5 = devBaseData('蒸发1A进',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('16_5', data16_5)

data16_6 = devBaseData('蒸发1A出',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('16_6', data16_6)

data16_7 = devBaseData('蒸发1B进',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('16_7', data16_7)

data16_8 = devBaseData('蒸发1B出',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('16_8', data16_8)

data16_9 = devBaseData('蒸发2A进',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('16_9', data16_9)

data16_10 = devBaseData('蒸发2A出',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('16_10', data16_10)

data16_11 = devBaseData('蒸发2B进',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('16_11', data16_11)

data16_12 = devBaseData('蒸发2B出',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('16_12', data16_12)

data16_13 = devBaseData('防冻1',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('16_13', data16_13)

data16_14 = devBaseData('防冻2',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('16_14', data16_14)

data16_15 = devBaseData('排气1',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('16_15', data16_15)

data16_16 = devBaseData('排气2',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('16_16', data16_16)

data25_1 = devBaseData('水泵模式',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_1', data25_1)

data25_2 = devBaseData('当前机号',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_2', data25_2)

data25_3 = devBaseData('系统数量',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_3', data25_3)

data25_4 = devBaseData('机组模式',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_4', data25_4)

data25_5 = devBaseData('空调防冻模式环温',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_5', data25_5)

data25_6 = devBaseData('防冻模式启动温度',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_6', data25_6)

data25_7 = devBaseData('防冻保护',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_7', data25_7)

data25_8 = devBaseData('掉电保护',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_8', data25_8)

data25_9 = devBaseData('主从机',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_9', data25_9)

data25_10 = devBaseData('喷淋阀开启',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_10', data25_10)

data25_11 = devBaseData('制冷模式选择',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_11', data25_11)

data25_12 = devBaseData('制冷初始开度',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_12', data25_12)

data25_13 = devBaseData('制冷最小开度',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_13', data25_13)

data25_14 = devBaseData('制冷过热度',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_14', data25_14)

data25_15 = devBaseData('制冷+热水 模式选择',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_15', data25_15)

data25_16 = devBaseData('制冷+热水 初始开度',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_16', data25_16)

data25_17 = devBaseData('制冷+热水 过热度',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_17', data25_17)

data25_18 = devBaseData('热水 模式选择',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_18', data25_18)

data25_19 = devBaseData('热水 初始开度',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_19', data25_19)

data25_20 = devBaseData('热水 过热度',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_20', data25_20)

data25_21 = devBaseData('热水 除霜开度',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_21', data25_21)

data25_22 = devBaseData('制热 模式选择',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_22', data25_22)

data25_23 = devBaseData('制热 初始开度',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_23', data25_23)

data25_24 = devBaseData('制热 过热度',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_24', data25_24)

data25_25 = devBaseData('制热 除霜开度',dataConstraint(1,1.0, None, None))
triplecng1.addDataItem('25_25', data25_25)

DisCountConstraint = dataConstraint(1,3.0,None,None)
DisCount = devBaseData('三联供1号机通信故障',DisCountConstraint)
triplecng1.addDataItem('DisCount',DisCount)

for k in sorted(triplecng1.getDataDict().keys()) :
    print k,triplecng1.getDataDict()[k]
    
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

for k in sorted(voc1.getDataDict().keys()) :
    print k,voc1.getDataDict()[k]
    
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


    

for k in sorted(wenkong1.getDataDict().keys()) :
    print k,wenkong1.getDataDict()[k]
    
wenkong1.setDisConnect(0)
print wenkong1.getDataDict()['DisCount']
print wenkong1.getDataDict()['DisCount'].Changed
    
wenkong1.setDisConnect(1)
print wenkong1.getDataDict()['DisCount']
print wenkong1.getDataDict()['DisCount'].Changed

for i in range(10) :
    wenkong1.setDisConnect(1)
    print wenkong1.getDataDict()['DisCount'].Changed
     
print wenkong1.getDataDict()['DisCount']
wenkong1.setDisConnect(0)
print wenkong1.getDataDict()['DisCount']
print wenkong1.getDataDict()['DisCount'].Changed