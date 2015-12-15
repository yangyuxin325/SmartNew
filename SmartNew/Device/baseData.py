#coding=utf8
'''
Created on 2015年6月16日

@author: sanhe
'''
from datetime import datetime
__metaclass__ = type

class dataConstraint():
    def __init__(self, data_owner, min_variation, min_val, max_val, dis_interval):
        self._data_owner = data_owner
        self._min_variation = min_variation
        self._min_val = min_val
        self._max_val = max_val
        self._dis_interval = dis_interval
        
    def __str__(self):
        return ('Data_Owner : %s, Min_Variation : %s,' +
        'Min_Value : %s, Min_Value : %s, Dis_Interval : %s') % (str(self._data_owner),
                                           str(self._min_variation),
                                           str(self._min_val),
                                           str(self._max_val),
                                           str(self._dis_interval))
        
    @property
    def Data_Owner(self):
        return self._data_owner
    
    @Data_Owner.setter
    def Data_Owner(self, value):
        self._data_owner = value
    
    @property
    def Min_Variation(self):
        return self._min_variation
    
    @Min_Variation.setter
    def Min_Variation(self, value):
        self._min_variation = value
    
    @property
    def Min_Value(self):
        return self._min_val
    
    @Min_Value.setter
    def Min_Value(self, value):
        self._min_val = value
    
    @property
    def Max_Value(self):
        return self._max_val
    
    @Max_Value.setter
    def Max_Value(self, value):
        self._max_val = value
    
    @property
    def Dis_Interval(self):
        return self._dis_interval
    
    @Dis_Interval.setter
    def Dis_Interval(self, value):
        self._dis_interval = value
    
class devdataConstraint(dataConstraint):
    def __init__(self, data_owner, min_variation, min_val, max_val, dis_interval, session_name, device_id, conf_name):
        dataConstraint.__init__(self, data_owner, min_variation, min_val, max_val, dis_interval)
        self._session_name = session_name
        self._device_id = device_id
        self._conf_name = conf_name
    
    def __str__(self):
        temp = ", Session_Name : %s, Device_id : %s, Conf_Name : %s" % (
                                                                      str(self._session_name),
                                                                      str(self._device_id),
                                                                      str(self._conf_name))
        return  dataConstraint.__str__(self) + temp
    
    @property
    def Session_Name(self):
        return self._session_name
    
    @Session_Name.setter
    def Session_Name(self, value):
        self._session_name = value

    @property
    def Device_id(self):
        return self._device_id
    
    @Device_id.setter
    def Device_id(self, value):
        self._device_id = value

    @property
    def Conf_Name(self):
        return self._conf_name
    
    @Conf_Name.setter
    def Conf_Name(self, value):
        self._conf_name = value

class basicData:
    def __init__(self, data_ename, data_cname, data_constraint=None):
        self._data_ename = data_ename
        self._data_cname = data_cname
        self._change_flag = False
        self._data_constraint = data_constraint
        self._Averge_datalist = []
        self._data_value = None
        self._error_flag = False
        self._time = None
        self._dis_flag = False
        self._distime = None
        
        self._write_value = None
        self._write_time = None
        self._reason = None
        
    @property   
    def Changed(self):
        return self._change_flag
        
    def addAverageData(self, data, minute):
        data_dict = {'total' : 0, 'count' : 0, 'sumT' : minute, 'Time' : None}
        self._Averge_datalist.append((data,data_dict))
        
    def initWriteValue(self, value, time):
        self._write_value = value
        self._write_time = time
        
    def setDisFlag(self, flag):
        if self._dis_flag != flag:
            self._dis_flag = flag
            self._distime = datetime.now()
            self._change_flag = True
            
    def setUpdateValue(self, value, time, error_flag, dis_flag, dis_time):
        self._value = value
        self._time = time
        self._error_flag = error_flag
        self._dis_flag = dis_flag
        self._distime = dis_time
        
    def setValue(self, value):
        if self._value is None :
            self._value = value
            self._change_flag = True
        else : 
            import math
            if math.fabs(self._value - value) >= self._contraint.Min_Variation :
                self._value = value
                self._change_flag = True
            else :
                self._change_flag = False
        
        if self._contraint.Min_Value < value < self._contraint.Max_Value :
            self._error_flag = False
        else:
            self._error_flag = True
                
        if self._Averge_datalist is not None and self._error_flag is False :
            for item in self._Averge_datalist:
                if item[1]['total'] == 0 :
                    item[1]['Time'] = datetime.now()
                item[1]['total'] += value
                item[1]['count'] += 1
                if (datetime.now() - item[1]['Time']).total_seconds() >= item[1]['sumT'] * 60 :
                    item[0].setValue(item[1]['total'] / item[1]['count'])
                    item[1]['total'] = 0
                    item[1]['count'] = 0
        self._time = datetime.now()
        if self._dis_flag is True:
            self._dis_flag = False
            self._distime = datetime.now()
            
    def getValue(self):
        if self._dis_flag is False and self._error_flag is False:
            return self._value
        elif self._dis_flag is True and self._error_flag is False:
            if (datetime.now() - self._distime).total_seconds() > self._data_constraint.Dis_Interval:
                return self._value
        
    def getRealValue(self):
        return self._value
    
    def setWriteValue(self, value):
        if self._write_value != value:
            self._write_value = value
            self._write_time = datetime.now()
    
    def setDataConstraint(self, value):
        self._data_constraint = value
        
    def setReason(self, value):
        self._reason = value
        
    
    
            
# obj = dataConstraint('first', 1, 2, 3, 5)
# obj1 = devdataConstraint('first', 1, 2, 3, 5, 'session1', 12, 'port1')
#         
# print obj
# print obj1
#  
# print type(obj),type(obj1)
#  
# print type(obj) == dataConstraint