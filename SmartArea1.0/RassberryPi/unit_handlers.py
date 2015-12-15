#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年10月9日

@author: sanhe
'''
import struct
import json

area_AProtocolhandlers = {}

def area_AHandleData(node_side):
    buf = node_side.recv(16)
    print buf.strip()
    if len(buf) == 16 :
        head = struct.unpack('!4i',buf)
        print head
        if head[3] > 0 :
            print 'MSGID : ', node_side.addr[0], head[2]
            buf = node_side.recv(head[3])
            if len(buf) == head[3] :
                body = json.loads(buf)
                print body
                try:
                    area_AProtocolhandlers[head[2]](head, body, node_side)
                except Exception as e:
                    print "area_AHandleData got Error : ", e
                    

def area_AHandleDevDatas(head, body, node_side):
    head = list(head)
    if body['status_code'] == 1:
        pass
    elif body['status_code'] == 255:
        pass
                   
area_AProtocolhandlers[9] = area_AHandleDevDatas