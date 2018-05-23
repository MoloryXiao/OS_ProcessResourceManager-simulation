'''
Created on 2018年5月19日

@author: Murrey
'''
from PCB import NewPCB

class ProcessManager(object):
    __currentPoint = None
    __maxPrio = 2
    
    def __init__(self,readyList,blockList):
        self.__readyList = readyList
        self.__blockList = blockList
        initPcb = NewPCB("init",0,"ready")
        self.__readyList[0].append(initPcb)    # 将新进程加入对应的就绪队列
        self.__scheduler()    # 进程调度
    
    def __getProcess(self,pid):
        for i in range(self. __maxPrio,-1,-1):
            for j in range(self.__readyList[i].__len__()):
                if self.__readyList[i][j].pid == pid :
                    return self.__readyList[i][j]
        return False
    
    def __countPCB(self):
        count =0
        for i in range(self.__readyList.__len__()):
            count += self.__readyList[i].__len__()
        return count
    
    def __killPCB(self,pcb):
        childNum = pcb.childTree.__len__()
        l_prio = pcb.prio
        if childNum == 0:            
            self.__readyList[l_prio].remove(pcb)
        else:
            for i in range(childNum):
                self.__killPCB(pcb.childTree[i])
            self.__readyList[l_prio].remove(pcb)
    
    def printReadyList(self):
        print("Proecess Counts：%d"%self.__countPCB())
        for i in range(self. __maxPrio,-1,-1):
            print("==========ReadyList_%d=========="%i)
            for j in range(self.__readyList[i].__len__()):
                self.__readyList[i][j].print()
    
    def createProcess(self,pid,prio):
        if self.__getProcess(pid) != False:
            print("Error: create process error.Pid has existed.")
            return
        if prio > self.__maxPrio:       # 优先级越界
            print("Error: create process error.Priority is illegal.")
            return
            
        newPcb = NewPCB(pid,prio,"ready") 
        if self.__currentPoint != None:    # 若是第一进程则直接加入就绪队列  若不是则与当前的运行进程建立关联
            self.__currentPoint.childTree.append(newPcb)    
            newPcb.parent = self.__currentPoint         
        self.__readyList[prio].append(newPcb)    # 将新进程加入对应的就绪队列
        self.__scheduler()    # 进程调度
        
    def destoryProcess(self,pid):
        desPcb = self.__getProcess(pid)
        if desPcb == None:
            print("Error: Don't have a process with this pid.Please check your input.")
            return
        else:
            parentPcb = desPcb.parent
            if parentPcb != None:       # 追溯到父进程 在子进程表中删除该进程
                parentPcb.childTree.remove(desPcb)
            self.__killPCB(desPcb)
        self.__scheduler()
    
    def timeOut(self):
        desPcb = self.__currentPoint
        if desPcb.prio == 0:
            print("Warning: Current Process is <init>. Can not be switched.")
            return
        self.__readyList[desPcb.prio].remove(desPcb) # 移除出队列
        self.__readyList[desPcb.prio].append(desPcb) # 加到队尾
        self.__scheduler()
    
    def __scheduler(self):
        if self.__countPCB() == 0:
            print("Nothing is running.")
        else:
            for i in range(self.__maxPrio,-1,-1):
                for j in range(self.__readyList[i].__len__()):
                    if self.__currentPoint == None:     # 若为第一进程则直接运行
                        self.__readyList[i][j].status = "running"
                        self.__currentPoint = self.__readyList[i][j]
                        print("Process %s is running."%self.__readyList[i][j].pid)   # 返回就绪队列中最高优先级的第一个进程
                        return
                    if (self.__readyList[i][j] != self.__currentPoint): # 若不为第一进程 且最高优先级进程不为当前进程 则切换执行进程
                        self.__currentPoint.status = "ready"
                        self.__readyList[i][j].status = "running"
                        self.__currentPoint = self.__readyList[i][j]                    
                        print("Process %s is running."%self.__readyList[i][j].pid)
                        return
                    else:   # 若最高优先级进程与当前进程一致 则不进行任何操作
                        return
            