'''
Created on 2018年5月23日

@author: Murrey
'''

class NewRcb(object):
    def __init__(self, rid , resSum):
        self.rid = rid
        self.sum = resSum
        self.available = resSum
        self.usingList = []
        self.waitingList = []
    
    ####
    # 函数功能：从等待队列中寻找可用的等待项 即申请的资源数可以被满足
    ####
    def findUsableWaitingItem(self):
        for i in range(self.waitingList.__len__()):
            if self.waitingList[i].num <= self.available:
                return self.waitingList[i]
        return False
    
    ####
    # 函数功能：判断PCB是否存在于资源的使用队列中
    ####
    def isPcbExistInUsingList(self,pcb):
        for i in range(self.usingList.__len__()):
            if self.usingList[i].pcb.pid == pcb.pid:
                return True
        return False
    
    ####
    # 函数功能：根据给定的PCB 从资源的使用队列中获取该项
    ####
    def getItemFromUsingList(self,pcb):
        for i in range(self.usingList.__len__()):
            if self.usingList[i].pcb.pid == pcb.pid:
                return self.usingList[i]
        return False
    
    ####
    # 函数功能：修改资源的使用队列中某项的信息
    ####
    def modifyUsingList(self,pcb,releaseNum):
        for i in range(self.usingList.__len__()):
            if self.usingList[i].pcb == pcb:
                self.usingList[i].num -= releaseNum
                if self.usingList[i].num == 0:
                    self.usingList.remove(self.usingList[i])
                return True
        return False
    
    ####
    # 函数功能：根据给定的PCB 从资源的等待队列中获取该项
    ####
    def getItemFromWaitingList(self,pcb):
        for i in range(self.waitingList.__len__()):
            if self.waitingList[i].pcb == pcb:
                return self.waitingList[i]
        return False
    
    ####
    # 函数功能：根据给定的PCB 从资源的等待队列中删除该项
    ####
    def deleItemFromWaitingList(self,pcb):
        for i in range(self.waitingList.__len__()):
            if self.waitingList[i].pcb == pcb:
                self.waitingList.remove(self.waitingList[i])
                return True
        return False
    
    ####
    # 函数功能：打印当前资源的基本情况
    ####
    def print(self):
        print("%s[%d/%d]"%(self.rid,self.available,self.sum),end=' ')
        print("[",end=' ')
        for i in range(self.waitingList.__len__()):
            print("%s "%self.waitingList[i].pcb.pid, end=' ')
        print("]")