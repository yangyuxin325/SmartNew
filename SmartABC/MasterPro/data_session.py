#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年12月4日

@author: sanhe
'''

class data_session():
    def __init__(self, session_name, com_id):
        self._session_name = session_name
        self._com_id = com_id
        
        
    def __str__(self):
        return 'session_name : %s, com_id : %s' % (str(self._session_name), 
                                                   str(self._com_id))