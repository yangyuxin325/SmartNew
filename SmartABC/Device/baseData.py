#coding=utf8
'''
Created on 2015年6月16日

@author: sanhe
'''
from datetime import datetime
from __builtin__ import str
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
    def __init__(self, data_ename, init_value, data_constraint=None):
        self._data_ename = data_ename
        self._data_value = init_value
        self._data_constraint = data_constraint
        
# obj = dataConstraint('first', 1, 2, 3, 5)
# obj1 = devdataConstraint('first', 1, 2, 3, 5, 'session1', 12, 'port1')
#         
# print obj
# print obj1
#  
# print type(obj),type(obj1)
#  
# print type(obj) == dataConstraint