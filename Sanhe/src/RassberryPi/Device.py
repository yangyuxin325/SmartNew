#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年4月27日

@author: sanhe
'''

import Dev_CmdPack

class device():
    device_type = 0
    def __init__(self,devid_id):
        self.devid_id = devid_id
    def get_device_id(self):
        return self.devid_id
    @classmethod
    def get_device_type(cls):
        return cls.device_type
    def get_routing_cmd(self):
        pass
    def get_send_cmd(self):
        pass
    def data_parse(self):
        pass
    
class infrared(device):
    device_type = 1
    def __init__(self,device_id):
        device.__init__(self, device_id)
    def get_device_id(self):
        return device.get_device_id(self)
    def get_routing_cmd(self):
        return Dev_CmdPack.infraredCmdPack1(self.devid_id)
    

    
print Dev_CmdPack.infraredCmdPack1(21)

    