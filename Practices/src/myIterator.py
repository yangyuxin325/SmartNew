 # -*- coding: UTF-8 -*-
'''
Created on 2015年1月10日

@author: sanhe
'''

class MyIterator(object):
    def __init__(self,step):
        self.step = step
        
    def next(self):
        """Return the next element."""
        if self.step == 0:
            raise StopIteration
        self.step -= 1
        return self.step
    
    def __iter__(self):
        """Returns the iterator itself."""
        return self
    
    
for el in MyIterator(4):
    print el
    
def fibonacci():
    a, b = 0, 1
    while True:
        yield b
        a, b = b, a+b
        
fib = fibonacci()

print fib.next()
    
print fib.next()

print fib.next()

print [fib.next() for i in range(10)]
