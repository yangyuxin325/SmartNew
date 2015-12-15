#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年7月8日

@author: sanhe
'''

class Base:
    def __init__(self):
        self.name = "Base"
        self.salary = 200
        
        
class Sub(Base):
    def __init__(self):
        Base.__init__(self)
        print self.name
        self.name = "Sub"


A = Base()
B = Sub()

print "---------------------------"
print A.name
print A.salary
print B.name
print B.salary
