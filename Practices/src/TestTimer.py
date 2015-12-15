#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年9月18日

@author: sanhe
'''

from threading import Timer  
import time  
  
timer_interval=1  
def delayrun():  
    print 'running'  
  
t=Timer(timer_interval,delayrun)  
t.start()  
while True:  
    time.sleep(0.1)  
    print 'main running'
    t.cancel()
