
class NewWaitingListItem(object):
    def __init__(self, pcb ,resNum):
        self.pcb = pcb
        self.num = resNum
pass

class NewUsingListItem(object):
    def __init__(self, pcb, num):
        self.pcb = pcb
        self.num = num
pass

class NewBlockingListItem(object):
    def __init__(self, pcb, rid):
        self.pcb = pcb
        self.rid = rid
    
    def print(self):
        print("%s[%s](%s)"%(self.pcb.pid,self.pcb.status,self.rid))
pass

class NewResourceItem(object):
    def __init__(self, rid ,num):
        self.rid = rid
        self.num = num
pass