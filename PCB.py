'''
Created on 2018年5月17日

@author: Murrey
'''

class NewPCB(object):
    def __init__(self, PID , Prio):
        self.pid = PID
        self.prio = Prio
        self.childTree = []
        self.resources = []
        self.status = None
        self.parent = None
        self.cpuState = None
        self.memory = None
        self.openFiles = None