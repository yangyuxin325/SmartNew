#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年7月2日

@author: sanhe
'''
import logging

logging.basicConfig(level = logging.DEBUG,
                    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt = '%d %b %Y %H:%M:%S',
                    filename = 'test.log',
                    filemode = 'w'
                    )

def datalog(func):
    def wrapper(arg1, arg2):
        self = arg1
        logging.info("received data : %s", str(arg2))
        func(arg1, arg2)
        for key, value in self.getDataDict().items() : 
            pass
#             logging.info("key : %s , value : %s" % (key, value))
    return wrapper