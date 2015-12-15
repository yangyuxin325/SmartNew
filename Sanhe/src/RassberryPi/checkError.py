#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年3月10日

@author: sanhe
'''

class PumpCheck(object):
    def __init__(self,name1,name2,name3):
        self.pump1 = name1
        self.pump2 = name2
        self.pump3 = name3
        
    def __call__(self,mysqlConnect):
        print "call PumpCheck : ", self.pump1, self.pump2, self.pump3