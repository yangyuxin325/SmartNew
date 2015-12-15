#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年12月7日

@author: sanhe
'''

class Server_Para():
    def __init__(self, stype, name, ip):
        self._type = stype  #type 1 区域 2 本身单元  3 节点连接上来 4 本身区域 5 单元  6本身节点
        self._name = name
        self._ip = ip
        
    @property
    def Server_Type(self):
        return self._type
    
    @property
    def Server_Name(self):
        return self._name
    
    @property
    def Server_Ip(self):
        return self._ip
    