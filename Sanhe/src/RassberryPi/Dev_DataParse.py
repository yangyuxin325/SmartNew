#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年3月12日

@author: sanhe
'''
def D_IOParse(port,data,mysqlConnect):
    D_IO_List = []
    for i in range(8*data[2]):
        if i < 8 :
            D_IO_List.append((data[3] & (1 << i)) >> i)
        else:
            D_IO_List.append((data[4] & (1 << (i - 8))) >> (i - 8))
    return D_IO_List

def AOparse(port,data,mysqlConnect):
    AO_List = []
    AO_List.append(data[3] << 8 + data[4])
    AO_List.append(data[5] << 8 + data[6])
    return AO_List

def AIParse(port,data,mysqlConnect):
    AI_List = []
    for i in range(data[2]/2):
        AI_List.append((data[i*2+3] << 8) + data[i*2+4])
    return AIParse

port_dict = {
             1 : D_IOParse,
             2 : D_IOParse,
             3 : AOparse,
             4 : AIParse
             }

port_type = {1 : 'DO',
             2 : 'DI',
             3 : 'AO',
             4 : 'AI'
             }

def plcDataParse(port,data,mysqlConnect):
    data_dict = {}
    i = 0
    for item in port_dict[data[1]](port,data,mysqlConnect):
        name = '%s%d' % (port_type[data[1]],i)
        data_dict[name] = item
        i += 1
    print 'Line%d PLC : ID=%d' % (port,data[0]),data_dict
    
def mokuaiDataParse(port,data,mysqlConnect):
    data_dict = {}
    i = 0
    for item in port_dict[data[1]](port,data,mysqlConnect):
        name = '%s%d' % (port_type[data[1]],i)
        data_dict[name] = item
    print 'Line%d MoKuai : ID=%d' % (port,data[0]),data_dict

def infraredDataParse(port,data,mysqlConnect):
    ywr_val = (data[3] & 3)
    led_val = ((data[3] & 12) >> 2)
    doorstate_val = (data[3] & 16) >> 4
    state_val = (data[3] & 32) >> 5
    infotime_val = (data[4] * 15000 + data[5] * 70)//1000
    data_dict = {}
    data_dict['YWR'] = ywr_val
    data_dict['LED'] = led_val
    data_dict['DoorState'] = doorstate_val
    data_dict['State'] = state_val
    data_dict['InfoTime'] = infotime_val
    print 'Line%d Infrared : ID=%d' % (port,data[0]),data_dict
    

def wenkongDataParse(port,data,mysqlConnect):
    onoff_val = data[4]
    mode_val = data[5] * 256 + data[6]
    settemp_val = data[7] + data[8]/10.0
    wind_val = data[9]*256 + data[10]
    temp_val = data[17] + data[18]/10.0
    data_dict = {}
    data_dict['OnOff'] = onoff_val
    data_dict['Mode'] = mode_val
    data_dict['SetTemp'] = settemp_val
    data_dict['Wind'] = wind_val
    data_dict['Temp'] = temp_val
    print 'Line%d WenKong : ID=%d' % (port,data[0]),data_dict

def sansuDataParse(port,data,mysqlConnect):
    wind_val = data[3]*256 + data[4]
    fa1_val = data[5]*256 + data[6]
    fa2_val = data[7]*256 + data[8]
    data_dict = {}
    data_dict['Wind'] = wind_val
    data_dict['Fa1'] = fa1_val
    data_dict['Fa2'] = fa2_val
    print 'Line%d SanSu : ID=%d' % (port,data[0]),data_dict

def co2DataParse(port,data,mysqlConnect):
    co2_val = data[3]*256 + data[4]
    data_dict = {}
    data_dict['CO2'] = co2_val
    print 'Line%d CO2 : ID=%d' % (port,data[0]),data_dict

def vocDataParse(port,data,mysqlConnect):
    voc_val = (data[3]*256 + data[4])/10.0
    temp_val = (data[5]*256 + data[6])/10.0
    hum_val = data[7]*256+data[8]
    data_dict = {}
    data_dict['VOC'] = voc_val
    data_dict['Temp'] = temp_val
    data_dict['Hum'] = hum_val
    print 'Line%d VOC : ID=%d' % (port,data[0]),data_dict

def triplecgnDataParse(port,data,mysqlConnect):
    para_dict = {
                 1 : ["温度补偿"],
                 2 : ["空调回水感温故障","空调出水感温故障","水箱感温故障","环境感温故障",
                      "防冻1感温故障","防冻2感温故障","排气1感温故障","排气2感温故障",
                      "蒸发1A进温故障","蒸发1A出温故障","蒸发1B进温故障","蒸发1B出温故障",
                      "蒸发2A进温故障","蒸发2A出温故障","蒸发2B进温故障","蒸发2B出温故障",
                      "系统1高压保护","系统1低压保护","系统1防冻保护","系统2高压保护",
                      "系统2低压保护","系统2防冻保护","空调水流故障","相序保护",
                      "进出水温差过大保护","冬季防冻保护","系统1排气过高保护",
                      "系统2排气过高保护","过热保护","热源测水流保护","空调模式防冻",
                      "系统其他保护（保留）"],
                 4 : ["电热启动环温","电热启动延时","电热启动温度","电热启动回差"],
                 5 : ["制冷设定","制热设定","水箱温度设定","空调回差设定","水箱回差设定"],
                 6 : ["开关机","模式","制冷设定","制热设定","热水设定"],
                 7 : ["除霜模式","进入温度","除霜周期","退出温度","除霜时间","除霜环境"],
                 15 : ["压缩机1","压缩机2","四通阀A","四通阀B","补水阀","风机","循环水泵",
                        "热水水泵","空调电加热","热水电加热","报警","系统1电子膨胀阀A",
                        "系统1电子膨胀阀B","系统2电子膨胀阀A","系统2电子膨胀阀B"],
                 16 : ["空调回水","空调出水","水箱","环境","蒸发1A进","蒸发1A出",
                       "蒸发1B进","蒸发1B出","蒸发2A进","蒸发2A出","蒸发2B进",
                       "蒸发2B出","防冻1","防冻2","排气1","排气2"],
                 25 : ["水泵模式","当前机号","系统数量","机组模式","空调防冻模式环温",
                       "防冻模式启动温度","房东保护","掉电保护","主从机","喷淋阀开启",
                       "制冷 模式选择","制冷 初始开度","制冷 最小开度","制冷 过热度",
                       "制冷+热水 模式选择","制冷+热水 初始开度","制冷+热水 过热度",
                       "热水 模式选择","热水 初始开度","热水 过热度","热水 除霜开度",
                       "制热 模式选择","制热 初始开度","制热 过热度","制热 除霜开度"]
                 }
    data_dict = {}
    if data[2]//2 == 5 :
        i = 0
        for item in para_dict[data[2]/2]:
            data_dict[para_dict[data[2]/2][i]] = (data[i*2+3] * 256 + data[i*2+4])//10
            i += 1
    elif data[2]//2 == 4:
        i = 0
        for item in para_dict[data[2]/2]:
            if i == 1 :
                data_dict[item] = data[i*2+3] * 256 + data[i*2+4]
            else:
                if 0xff == data[i*2+3]:
                    data_dict[item] = (data[i*2+3]*256 + data[i*2+4] - 65536)//10
                else:
                    data_dict[item] = (data[i*2+3]*256 + data[i*2+4])//10
            i += 1
    elif data[2]//2 == 7:
        i = 0
        for item in para_dict[data[2]/2]:
            if 0 == i or 2 == i or 4 == i :
                data_dict[item] = data[i*2+3] * 256 + data[i*2+4]
            else:
                if 0xff == data[i*2+3]:
                    data_dict[item] = (data[i*2+3]*256 + data[i*2+4] - 65536)//10
                else:
                    data_dict[item] = (data[i*2+3]*256 + data[i*2+4])//10
            i += 1
    elif data[2]//2 == 25:
        i = 0
        for item in para_dict[data[2]/2]:
            if 5<= i <= 6 or 9 == i or 13 == i or 17 == i or 24 == i:
                if 0xff == data[i*2+3]:
                    data_dict[item] = (data[i*2+3*256] + data[i*2+4] - 65536)//10
                else:
                    data_dict[item] = (data[i*2+3]*256 + data[i*2+4])//10
            else:
                data_dict[item] = data[i*2+3] * 256 + data[i*2+4]
            i += 1
    elif data[2]//2 == 1:
        i = 0
        for item in para_dict[data[2]/2]:
            data_dict[item] = data[i*2+3] * 256 + data[i*2+4]
            i += 1
    elif data[2]//2 == 16:
        i = 0
        for item in para_dict[data[2]/2]:
            data_dict[item] = (data[i*2+3] * 256 + data[i*2+4])//10
            i += 1
    elif data[2]//2 == 15:
        i = 0
        for item in para_dict[data[2]/2]:
            data_dict[item] = data[i*2+3] * 256 + data[i*2+4]
            i += 1
    elif data[2]//2 == 2:
        for i in range(len(para_dict[2])):
            if i < 8:
                data_dict[para_dict[2][i+8]] = ((data[3] & (1 << i)) >> i) 
            elif i < 16:
                data_dict[para_dict[2][i-8]] = ((data[4] & (1 << (i-8))) >> (i-8))
            elif i < 24:
                data_dict[para_dict[2][i+24]] = ((data[5] & (1 << (i-16))) >> (i-16))
            else:
                data_dict[para_dict[2][i+16]] = ((data[6] & (1 << (i-24))) >> (i-24))
                
    print 'Line%d TipleCNG : ID=%d' % (port,data[0])
    for key,value in data_dict.items():
        print key,value

DataParseFunc = {'plc' : plcDataParse,
                 'mokuai' : mokuaiDataParse,
                 'infrared' : infraredDataParse,
                 'wenkong' : wenkongDataParse,
                 'sansu' : sansuDataParse,
                 'co2' : co2DataParse,
                 'voc' : vocDataParse,
                 'triplecgn' :triplecgnDataParse}