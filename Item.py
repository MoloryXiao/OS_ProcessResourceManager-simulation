####
# 类功能：用于资源的等待队列
####
class NewWaitingListItem(object):
    def __init__(self, pcb ,resNum):
        self.pcb = pcb
        self.num = resNum
pass

####
# 类功能：用于资源的使用队列
####
class NewUsingListItem(object):
    def __init__(self, pcb, num):
        self.pcb = pcb
        self.num = num
pass

####
# 类功能：用于资源管理器的阻塞队列
####
class NewBlockingListItem(object):
    def __init__(self, pcb, rid):
        self.pcb = pcb
        self.rid = rid
    
    def print(self):
        print("%s[%s](%s)"%(self.pcb.pid,self.pcb.status,self.rid))
pass

####
# 类功能：用于存储申请到的资源
####
class NewResourceItem(object):
    def __init__(self, rid ,num):
        self.rid = rid
        self.num = num
pass