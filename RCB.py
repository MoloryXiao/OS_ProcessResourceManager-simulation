'''
Created on 2018年5月23日

@author: Murrey
'''
from Item import NewUsingListItem, NewWaitingListItem

class NewRcb(object):
    def __init__(self, rid , resSum):
        self.rid = rid
        self.sum = resSum
        self.available = resSum
        self.usingList = []
        self.waitingList = []
        
    def isPcbExistInUsingList(self,pcb):
        for i in range(self.usingList.__len__()):
            if self.usingList[i].pcb.pid == pcb.pid:
                return True
        return False
    
    def getPcbFromUsingList(self,pcb):
        for i in range(self.usingList.__len__()):
            if self.usingList[i].pcb.pid == pcb.pid:
                return self.usingList[i]
        return False
    
    def modifyUsingList(self,pcb,releaseNum):
        for i in range(self.usingList.__len__()):
            if self.usingList[i].pcb.pid == pcb.pid:
                self.usingList[i].num -= releaseNum
                if self.usingList[i].num == 0:
                    self.usingList.remove(self.usingList[i])
                return True
        return False
    
    def findUsableWaitingItem(self):
        for i in range(self.waitingList.__len__()):
            if self.waitingList[i].num <= self.available:
                return self.waitingList[i]
        return False
    
    def getItemFromWaitingList(self,pcb):
        for i in range(self.waitingList.__len__()):
            if self.waitingList[i].pcb == pcb:
                return self.waitingList[i]
        return False
    
    def deleItemFromWaitingList(self,pcb):
        for i in range(self.waitingList.__len__()):
            if self.waitingList[i].pcb == pcb:
                self.waitingList.remove(self.waitingList[i])
                return True
        return False
    
    def print(self):
        print("%s[%d/%d]"%(self.rid,self.available,self.sum),end=' ')
        print("[",end=' ')
        for i in range(self.waitingList.__len__()):
            print("%s "%self.waitingList[i].pcb.pid, end=' ')
        print("]")