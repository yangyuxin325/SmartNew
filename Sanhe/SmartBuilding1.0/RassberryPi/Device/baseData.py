#coding=utf8
'''
Created on 2015年6月16日

@author: sanhe
'''
from datetime import datetime
__metaclass__ = type

class dataConstraint():
    def __init__(self, state, min_variation, min_val, max_val):
        self._state = state
        self._min_variation = min_variation
        self._min_val = min_val
        self._max_val = max_val
        
    @property
    def State(self):
        return self._state
    
    @property
    def Min_Variation(self):
        return self._min_variation
    
    @property
    def Min_Value(self):
        return self._min_val
    
    @property
    def Max_Value(self):
        return self._max_val
    
        
class devBaseData():
    def __init__(self, name, constraint):
        self._name = name
        self._value = None
        self._contraint = constraint
        self._next_data = None
        self._Averge_datalist = []
        self._change_flag = False
        self._error_flag  = False
        self._time = None
    
    def __sub__(self, other):
        return self._value - other.DataValue
    
    @property
    def Value(self):
        return (self._name, self._value, self._time)
    
    @property
    def Name(self):
        return self._name
    
    def __str__(self):
        return "DataName = " + self._name + ", " \
            + "Value = " + str(self._value) + ", " \
            + "UpdateTime = " + str(self._time)
         
    @property   
    def Changed(self):
        return self._change_flag
    
    @property
    def DataState(self):
        return self._contraint.State    
    
    @property
    def DataValue(self):
        return self._value
                
    def addExceptData(self, data):
        self._next_data = data
        
    def addAverageData(self, data, minute):
        data_dict = {'total' : 0, 'count' : 0, 'sumT' : minute, 'Time' : None}
        self._Averge_datalist.append((data,data_dict))
    
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
            
        if self._next_data is not None :
            if self._contraint.Min_Value < value < self._contraint.Max_Value :
                self._next_data.setValue(0)
                self._error_flag = False
            else :
                self._next_data.setValue(1)
                self._error_flag = True
                
        if self._Averge_datalist is not None and self._error_flag == False :
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
        
# dc = dataConstraint(1,0.5,-50.0,50.0)
# data1 = devBaseData('name1', dc)
# dc = dataConstraint(1,1,None,None)
# data2 = devBaseData('name1_Error',dc)
# data1.addExceptData(data2)
# dc = dataConstraint(1,0.2,None,None)
# data3 = devBaseData('name1_1M',dc)
# data1.addAverageData(data3,1)
# data4 = devBaseData('name1_5M',dc)
# data1.addAverageData(data4,5)
# 
# import random
# from time import sleep
# print data1
# print data2
# print data3
# print data4
# 
# for i in range(600):
#     data1.setValue(random.uniform(20,30))
#     if i%2 == 0 :
#         data1.setValue(-50.2)
#     sleep(1)
#     print data1
#     print data2
#     print data3
#     print data4