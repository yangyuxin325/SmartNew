#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年3月12日

@author: sanhe
'''

line0dict = {
             21 : 'infrared',
             22 : 'infrared',
             23 : 'infrared',
             24 : 'infrared',
             11 : 'plc', 
             12 : 'mokuai', 
             1 : 'sansu',
             2 : 'sansu',
             3 : 'sansu',
             4 : 'sansu',
             5 : 'sansu',
             6 : 'sansu',
             7 : 'sansu',
             8 : 'sansu',
             9 : 'sansu',
             16 : 'sansu',
             17 : 'sansu',
             18 : 'sansu',
             19 : 'sansu',
             20 : 'sansu'
             }

line1dict = {
#              21 : 'infrared',
#              22 : 'infrared',
#              23 : 'infrared',
#              24 : 'infrared',
#              11 : 'plc', 
#              12 : 'mokuai', 
#              13 : 'plc', 
#              14 : 'plc', 
#              15 : 'mokuai',
            16 : 'triplecgn',
            17 : 'triplecgn',
            18 : 'triplecgn',
            19 : 'triplecgn'
             }

line2dict = {
             21 : 'infrared',
             23 : 'infrared',
             24 : 'infrared',
             25 : 'infrared',
             26 : 'infrared',
             27 : 'infrared',
             28 : 'infrared',
             29 : 'infrared',
             32 : 'wenkong',
             35 : 'wenkong',
             1 : 'sansu',
             3 : 'sansu',
             4 : 'sansu',
             5 : 'sansu',
             6 : 'sansu',
             7 : 'sansu',
             8 : 'sansu',
             9 : 'sansu',
             33 : 'co2', 
             34 : 'voc'
             }

line3dict = {
             21 : 'infrared',
             23 : 'infrared',
             24 : 'infrared',
             25 : 'infrared',
             32 : 'wenkong',
             35 : 'wenkong',
             1 : 'sansu',
             3 : 'sansu',
             4 : 'sansu',
             5 : 'sansu',
             6 : 'sansu',
             33 : 'co2', 
             34 : 'voc'
             }

# MCSet = {0 : line0dict,
#          1 : line1dict,
#          2 : line2dict,
#          3 : line3dict}

MCSet = {
        3 : line0dict,
         2 : line1dict,
        0 : line2dict,
        1 : line3dict
         }


SerialSet = {
             '/dev/ttyUSB0' : 0 ,
             '/dev/ttyUSB1' : 1 ,
             '/dev/ttyUSB2' : 2 ,
             '/dev/ttyUSB3' : 2 ,
             }

from Dev_CmdPack import *

CmdSet = {}
for key,value in MCSet.items():
    line_cmdList = []
    cmdCount = 0
    for dev_id,dev_name in value.items():
        if dev_name in PackArrayConfig:
            arr = PackArrayConfig[dev_name]
            for data in arr:
                cmdCount += 1
                line_cmdList.append({"id" : (++cmdCount), "cmd" : CmdPackConfig[dev_name](dev_id,data), "nbcount" : 0})
        else:
            cmdCount += 1
            line_cmdList.append({"id" : (++cmdCount), "cmd" : CmdPackConfig[dev_name](dev_id), "nbcount" : 0})
            
    CmdSet[key] = line_cmdList
    
for key,value in CmdSet.items():
    print "line : %d" % key
    for item in value:
        print item
        
        
Serial_DevCmdSet_Config = {
                     '/dev/ttyUSB0' : CmdSet[SerialSet['/dev/ttyUSB0']],
                     '/dev/ttyUSB1' : CmdSet[SerialSet['/dev/ttyUSB1']],
                     '/dev/ttyUSB2' : CmdSet[SerialSet['/dev/ttyUSB2']],
                     '/dev/ttyUSB3' : CmdSet[SerialSet['/dev/ttyUSB3']]
                     }

            
        