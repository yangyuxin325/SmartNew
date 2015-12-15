#coding=utf8
'''
Created on 2015年3月6日

@author: sanhe
'''

from multiprocessing.connection import Listener
from array import array

address = ('localhost', 6000)
listener = Listener(address, authkey='secret password')

conn = listener.accept()
print 'connection accepted from', listener.last_accepted
 
conn.send([2.25, None, 'junk', float])
 
conn.send_bytes('hello')
 
conn.send_bytes(array('i',[42, 1729]))
 
conn.close()
Listener.close()