#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年3月13日

@author: sanhe
'''
from SmartServer import SmartServer

def SendHardCMD(SerialName, Cmd):
    session = SmartServer().getSession(SerialName)
    session.AddSendCmd(Cmd)
    
def sendTask(StartTime, Task):
    SmartServer().addTask(StartTime,Task)