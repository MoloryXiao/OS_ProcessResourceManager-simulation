'''
Created on 2018年5月17日

@author: Murrey
'''

class NewPCB(object):
    def __init__(self, PID , Prio, Status):
        self.pid = PID
        self.prio = Prio
        self.childTree = []
        self.resources = []
        self.status = Status
        self.parent = None
        self.cpuState = None
        self.memory = None
        self.openFiles = None
        
    def findResource(self,rid):
        for i in range(self.resources.__len__()):
            if self.resources[i].rid == rid:
                return self.resources[i]
        return False
      
    def modifyResourceNum(self,rid,num):
        for i in range(self.resources.__len__()):
            if self.resources[i].rid == rid:
                self.resources[i].num += num
                if self.resources[i].num == 0:
                    self.resources.remove(self.resources[i])
                return True
        return False
        
          
    def print(self):
        print("%s[%s]"%(self.pid,self.status),end=' ')
        print("[",end=' ')
        for i in range(self.resources.__len__()):
            print("%s(%d) "%(self.resources[i].rid,self.resources[i].num), end=' ')
        print("]")