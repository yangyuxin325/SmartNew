#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年3月11日

@author: sanhe
'''
from SmartConfig import MCSet
from SmartConfig import SerialSet
from Dev_DataParse import DataParseFunc

# print DataParseFunc[MCSet[SerialSet['/dev/ttyUSB0']][1]]("")

def dataEntrance(dataitem,mysqlConnect):
    port = dataitem[0]
    data = dataitem[1]
    print dataitem, len(dataitem[1])
    try:
        if ord(data[0]) == 0x99:
            DataParseFunc['infrared'](SerialSet[port],data,mysqlConnect)
        else:
            DataParseFunc[MCSet[SerialSet[port]][ ord(data[0])]](SerialSet[port],data,mysqlConnect)
    except Exception as e:
        print "dataEntrance Error :", e