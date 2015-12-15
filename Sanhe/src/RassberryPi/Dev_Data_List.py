#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年4月27日

@author: sanhe
'''

class Dev_Cmd():
    def __init__(self):
        self.cmd_id = 0
        self.cmd = None
        self.nbcount = 0
        
    def get_id(self):
        return self.cmd_id
    def set_id(self,cmd_id):
        self.cmd_id =cmd_id
        
    def get_cmd(self):
        return self.cmd
    def set_cmd(self,cmd):
        self.cmd = cmd
        
    def get_nbcount(self):
        return self.nbcount
    def set_nbcount(self,nbcount):
        self.nbcount = nbcount

class Data_List():
    def __init__(self):
        self.cmd_id = 0
        self.cmd_list = []
    
    def append_cmd(self,dev_cmd):
        dev_cmd.set_id(++self.cmd_id)
    

    