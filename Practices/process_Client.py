#coding=utf8
'''
Created on 2015年3月6日

@author: sanhe
'''
from multiprocessing.connection import Client
from array import array

address = ('localhost', 6000)
conn = Client(address, authkey='secret password')

print conn.recv()

print conn.recv_bytes()

arr = array('i',[0, 0, 0, 0, 0])
print conn.recv_bytes_into(arr)
print arr

conn.close()
