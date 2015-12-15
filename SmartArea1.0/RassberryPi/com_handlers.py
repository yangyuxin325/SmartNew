#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年8月7日

@author: sanhe
'''

def doSessionState(session, state):
    from handlers import hanldeSessionState
    session.putResultQueue(hanldeSessionState, {'session_name' : session.Name, 'session_state' : state})
    
# from deviceSet import deviceSet
# deviceSet().getDeviceSet()
# deviceSet().getDeviceName(dev_id)

def doDataProcess(session):
    try :
        devicedatas = session.getDeviceData()
#         print "doDataProcess: SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"
        for dev_id ,device in devicedatas.getDeviceSet().items():
            dev_name = devicedatas.getDeviceName(dev_id)
#             print dev_name, "__________________________________________________________________"
            dataDict = device.getDataDict()
#             print "doDataProcess  GETDISCOUNT VALUE IS" , device.GetDisCount()
            from handlers import handleDataChanged
            if device.GetDisCount() != 0 :
                if 'DisCount' in dataDict:
                    value = device.getDataDict()['DisCount']
                else:
                    return
                if value.Changed:
#                     print "DICOUNT ERROR : ", value
                    dataarray = []
                    dataarray.append(value.getDataItem())
                    session._device_set.setDisConnect(dev_id,device.GetDisCount())
                    session.putResultQueue(handleDataChanged,{'data' : dataarray, 'dev_name' : dev_name, 'session_name' : session.Name})
            else:
#                 print "DATADICT : XXXXXXXXXXXXXXXXX", dev_name,len(dataDict)
                for conf_name,value in dataDict.items():
#                     print conf_name, value
                    if value and value.Changed:
#                         print "DATA IS CHANGED : ", value
                        dataarray = []
                        dataarray.append(value.getDataItem())
                        session.putResultQueue(handleDataChanged,{'data' : dataarray, 'dev_name' : dev_name, 'session_name' : session.Name})
#             print "__________________________________________________________________END"
    except Exception as e:
        print "doDataProcess got Error : ", e,
        
        
def doFinishPeriod(session,periods):
    pass