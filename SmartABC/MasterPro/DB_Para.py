#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年12月7日

@author: sanhe
'''

class DB_Para():
    def __init__(self, addr, name, user, password):
        self._addr = addr
        self._name = name
        self._user = user
        self._password = password
        
    @property
    def DB_Addr(self):
        return self._addr
    
    @property
    def DB_Name(self):
        return self._name
    
    @property
    def DB_User(self):
        return self._user
    
    @property
    def DB_password(self):
        return self._password
    