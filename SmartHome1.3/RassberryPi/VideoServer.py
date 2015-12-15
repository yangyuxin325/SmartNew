#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年8月31日

@author: sanhe
'''

class VideoIPC():
    
    def __init__(self, ip, url, fps, rln, streamsize, state = 0):
        self._Data_Dict = {}
        self._Data_Dict['ip'] = ip
        self._Data_Dict['url'] = url
        self._Data_Dict['fps'] = fps
        self._Data_Dict['resolution'] = rln
        self._Data_Dict['streamsize'] = streamsize
        self._state = state
        
    def SetState(self, state):
        self._state = state
        return True
        
    def State(self):
        return self._state
    
    def setProperty(self, name, value):
        if name in self._Data_Dict:
            self._Data_Dict[name] = value
            return True
        return False
    
    def getProperty(self, name):
        if name in self._Data_Dict:
            return self._Data_Dict[name]
    
    def GetIPCProperties(self):
        return self._Data_Dict

class VideoServer():
    
    def __init__(self, server_ip, disk_space = 0, server_state = 0, server_name = None):
        self._server_ip = server_ip
        self._disk_space = disk_space
        self._server_state = server_state
        self._IPC_Map = {}
        self._server_name = None
        if server_name is not None:
            self._server_name = server_name
        self._recordSaveDays = None
        self._startFlag = 0
        
    def setStartFlag(self, flag):
        self._startFlag = flag
        
    def getStartFlag(self):
        return self._startFlag
            
    def setName(self, name):
        self._server_name = name
        return True
    
    def getName(self):
        return self._server_name
    
    def getIp(self):
        return self._server_ip
    
    def getDiskSpace(self):
        return self._disk_space
    
    def setDiskSpace(self, value):
        self._disk_space = value
    
    def setIPCProperty(self, ipc_name, name, value):
        if ipc_name in self._IPC_Map:
            if self._IPC_Map[ipc_name].setProperty(name, value):
                return True
        return False
    
    def setIPCState(self, ipc_name, state):
        if ipc_name in self._IPC_Map:
            if self._IPC_Map[ipc_name].SetState(state):
                return True
        return False
    
    def getIPCState(self, ipc_name):
        if ipc_name in self._IPC_Map:
            return self._IPC_Map[ipc_name].State()
        return False
    
    def getIPCs(self):
        return self._IPC_Map
        
    def addIPC(self, ipc_name, ipc):
        if ipc_name in self._IPC_Map:
            return False
        for name, ipcitem in self._IPC_Map.items():
            if ipcitem.getProperty('ip') == ipc.getProperty('ip'):
                del self._IPC_Map[name]
        if ipc_name is not None and cmp(ipc_name, "") != 0:
            self._IPC_Map[ipc_name] = ipc
            return True
        
    def delIPC(self, ipc_name):
        if ipc_name in self._IPC_Map:
            del self._IPC_Map[ipc_name]
            return True
        return False
    
    def SetRecordSaveDays(self, savedays):
        self._recordSaveDays = savedays
        return True
    
    def GetRecordSaveDays(self):
        return self._recordSaveDays
    
    def SetState(self, state):
        self._server_state = state
        
    def State(self):
        return self._server_state
    
class videoService():
    videoservers_map = {}
    videoNameIP_Dict = {}
    local_name =  None
    
    def __new__(cls, *args, **kwarg):
        if not cls.instance:
            cls.instance = super(videoService, cls).__new__(cls, *args, **kwarg)
        return cls.instance
    
    def Init(self,local_name):
        self.__class__.local_name = local_name
        ipc = VideoIPC("172.16.1.101","rtsp://admin:admin@172.16.1.101:554/cam/realmonitor?channel=1&subtype=0",
                       25,"1280*720",2048)
        self.addVideoServer("172.16.1.23", 0, 0, u"西山摄像服务器1")
        self.addVideoIPC("172.16.1.23", "ipc1", ipc)
        self.updateVideoSeverRecordDays(u"西山摄像服务器1", 30)
        ipc = VideoIPC("172.16.1.102","rtsp://admin:admin@172.16.1.102:554/cam/realmonitor?channel=1&subtype=0",
                       25,"1280*720",2048)
        self.addVideoServer("172.16.1.43", 0, 0, u"西山摄像服务器2")
        self.addVideoIPC("172.16.1.43", "ipc2", ipc)
        self.updateVideoSeverRecordDays(u"西山摄像服务器2", 30)

    def getVideoServerStartFlag(self, server_name):
        if server_name in self.videoNameIP_Dict:
            server_ip = self.videoNameIP_Dict[server_name]
            return self.videoservers_map[server_ip].getStartFlag()
        
    def setVideoServerStartFlag(self, server_name, flag):
        if server_name in self.videoNameIP_Dict:
            server_ip = self.videoNameIP_Dict[server_name]
            self.videoservers_map[server_ip].setStartFlag(flag)
        
    def addVideoServer(self, server_ip, disk_space= 0, server_state = 0, server_name = None):
        if server_ip not in self.videoservers_map and server_name not in self.videoNameIP_Dict:
            self.videoservers_map[server_ip] = VideoServer(server_ip,disk_space,server_state,server_name)
            if server_name is not None:
                self.videoNameIP_Dict[server_name] = server_ip
            return True
        return False
    
    def updateVideoServerName(self,server_ip,server_name):
        if server_ip in self.videoservers_map:
            videoserver = self.videoservers_map[server_ip]
            oldname = videoserver.getName()
            if oldname == server_name:
                return False
            if oldname is not None:
                del self.videoNameIP_Dict[videoserver.getName()]
            self.videoservers_map[server_ip].setName(server_name)
            self.videoNameIP_Dict[server_name] = server_ip
            return True
        return False
        
    def getVideoServerName(self,server_ip):
        if server_ip in self.videoservers_map:
            return self.videoservers_map[server_ip].getName()
        
    def getVideoServer(self, server_name):
        if server_name in self.videoNameIP_Dict:
            server_ip = self.videoNameIP_Dict[server_name]
            if server_ip in self.videoservers_map:
                return self.videoservers_map[server_ip]
    
    def delVideoServer(self, server_name):
        if server_name in self.videoNameIP_Dict:
            server_ip = self.videoNameIP_Dict[server_name]
            del self.videoNameIP_Dict[server_name]
            self.videoservers_map[server_ip].setName(None)
            return True
        return False
    
    def updateVideoServerDiskSpace(self, server_ip, value):
        if server_ip in self.videoservers_map:
            if self.videoservers_map[server_ip].getDiskSpace() != value:
                self.videoservers_map[server_ip].setDiskSpace(value)
                return True
        return False
    
    def getVideoServerDiskSpace(self, server_ip):
        if server_ip in self.videoservers_map:
            return self.videoservers_map[server_ip].getDiskSpace()
    
    def setVideoServerState(self, server_ip, state):
        if server_ip in self.videoservers_map:
            self.videoservers_map[server_ip].SetState(state)
            return True
        return False
            
    def getVideoServerState(self, server_ip):
        if server_ip in self.videoservers_map:
            return self.videoservers_map[server_ip].State()
        
    def updateVideoSeverRecordDays(self, server_name, days):
        if server_name in self.videoNameIP_Dict:
            server_ip = self.videoNameIP_Dict[server_name]
            if self.videoservers_map[server_ip].SetRecordSaveDays(days):
                return True
        return False
            
    
    def addVideoIPC(self, server_ip, ipc_name, ipc):
        if server_ip in self.videoservers_map:
            if self.videoservers_map[server_ip].addIPC(ipc_name, ipc) :
                return True
        return False
    
    def delVideoIPC(self, server_ip, ipc_name):
        if server_ip in self.videoservers_map:
            if self.videoservers_map[server_ip].delIPC(ipc_name):
                return True
        return False
    
    def setVideoIPCState(self, server_name, ipc_name, state):
        if server_name in self.videoNameIP_Dict:
            server_ip = self.videoNameIP_Dict[server_name]
            if server_ip in self.videoservers_map:
                self.videoservers_map[server_ip].setIPCState(ipc_name, state)
            
    def getVideoIPCState(self, server_name, ipc_name):
        if server_name in self.videoNameIP_Dict:
            server_ip = self.videoNameIP_Dict[server_name]
            if server_ip in self.videoservers_map:
                return self.videoservers_map[server_ip].getIPCState(ipc_name)
        
    def updateIPCProperty(self, server_ip, ipc_name, name, value):
        if server_ip in self.videoservers_map:
            self.videoservers_map[server_ip].setIPCProperty(ipc_name, name, value)