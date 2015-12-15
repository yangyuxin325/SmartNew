#coding=utf-8
#!/usr/bin/env python

'''
Created on 2015年2月5日

@author: sanhe
'''
from Smartserver import SmartServer
import serial.tools.list_ports

def main():
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) <= 0:
        print "There is not Serial port in the system"
    else:
        total_session = len(port_list)
        data = []
        instance = SmartServer(data,0.5)
        instance.start()

from multiprocessing import Process
from uuid import uuid4
import time

class TProcess(Process):
    def __init__(self):
        Process.__init__(self)
        
    def run(self):
        while True:
            time.sleep(1)
            with open(r'd:tprocess', u'a') as f:
                f.write(u'%s %s \n' % (self.name, uuid4()))


if __name__ == '__main__':
    print "Sanhe's raspberry pi software is starting!"
    try:
#         main()
        t = TProcess()
        t.daemon = True
        t.start()
        t.join()
        print u'to sleep'
        time.sleep(3)
        print u'sleep finished'
        print u'...'
    except Exception as e:
        print "catch finally00 exception." 
        print u'xxx'
        raise e