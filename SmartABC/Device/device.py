#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年7月8日

@author: sanhe
'''

device_Dict = {}

class device():
    
    def __init__(self, dev_id, dev_type):
        self._dev_id = dev_id
        self._dev_type = dev_type
        self._datadict = {
                    }
        self._otherkeys = {}
        self._connect_Flag = True
        self._disCount = 0
        
    def __str__(self):
        return 'device_type : %s, device_id : %s' % (str(self._dev_type),
                                                     str(self._dev_id))
        
    def GetDisCount(self):
        return self._disCount
        
    def getDataDict(self):
        for key,value in self._otherkeys.items():
            self.getOtherData(value, key)
        import copy
        return copy.deepcopy(self._datadict)
    
    def getOtherData(self,link_key, key):
        data = self._datadict[link_key].getOtherValue(key)
        self._datadict.update({key : data})
        
    def addDataItem(self, key, item):
        if key not in self._datadict.keys() :
            return
        self._datadict.update({key : item})
        
    def addExceptDataItem(self, key, item, link_key):
        if link_key not in self._datadict.keys() :
            return
        value = self._datadict[link_key]
        if value is not None :
            value.addExceptData(key, item)
            self._otherkeys.update({key : link_key})
            
    def addAverageDataItem(self, key, item, link_key, minute):
        if link_key not in self._datadict.keys() :
            return
        value = self._datadict[link_key]
        if value is not None :
            value.addAverageData(key, item, minute)
            self._otherkeys.update({key : link_key})
        
    @classmethod
    def genPratrolInstr(self, ID):
        pass
    
    def dataParse(self, data):
        pass
        
    def setDisConnect(self, value):
        data = self._datadict['DisCount']
        if data is None:
            return
        if data.DataValue is None :
            self._setDataValue('DisCount',0)
        if value == 1 :
                self._disCount = self._disCount + value
        elif value == 0:
            self._disCount = 0
        self._setDataValue('DisCount',self._disCount)
        if data is not None :
            if data.Changed :
                if data.DataValue > 1 :
                    self._connect_Flag = False
                else:
                    self._connect_Flag = True
        
    def _setDataValue(self, dataname, value):
        if dataname in self._datadict.keys() :
            if self._datadict[dataname] is not None:
                self._datadict[dataname].setValue(value)
            
    def getDataValue(self, dataname):
        if dataname in self._datadict.keys() :
            return self._datadict[dataname].DataValue
        elif dataname in self._otherkeys.keys() : 
            return self._datadict[self._otherkeys[dataname]].DataValue
        else :
            err = "There is not a {} data".format(dataname)
            raise Exception(err)

    def DisConnected(self):
        return self._connect_Flag    
