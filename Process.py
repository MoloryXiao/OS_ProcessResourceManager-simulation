'''
Created on 2018年5月19日

@author: Murrey
'''
from PCB import NewPCB
from _overlapped import NULL
class ProcessManager(object):
    __currentPoint = 0
    __maxPrio = 2
    __readyList = [ [] for i in range(3) ]
    __blockList = []
    def __init__(self):
        pass
    
    def __getProcess(self,pid):
        for i in range(self. __maxPrio,-1,-1):
            for j in range(self.__readyList[i].__len__()):
                if self.__readyList[i][j].pid == pid :
                    return self.__readyList[i][j]
        return NULL
    
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
        pass
    
    def printReadyList(self):
        print("Proecess Counts：%d"%self.__countPCB())
        for i in range(self. __maxPrio,-1,-1):
            print("==========ReadyList_%d=========="%i)
            for j in range(self.__readyList[i].__len__()):
                self.__readyList[i][j].print()
            print()     # 换行
    
    def createProcess(self,pid,prio):
        if self.__getProcess(pid) != False:
            print("Error: create process error.Pid has existed.")
            return
        if prio > self.__maxPrio:       # 优先级越界
            print("Error: create process error.Priority is illegal.")
            return
            
        newPcb = NewPCB(pid,prio)
        newPcb.status = "ready"
        if self.__currentPoint == 0:    # 第一进程
            self.__currentPoint = newPcb
        else:
            self.__currentPoint.childTree.append(newPcb)    # 将新进程与当前进程进行关联
            newPcb.parent = self.__currentPoint         
        self.__readyList[prio].append(newPcb)    # 将新进程加入对应的就绪队列
        self.__scheduler()    # 进程调度
    
    
    def destoryProcess(self,pid):
        desPcb = self.__getProcess(pid)
        if desPcb == NULL:
            print("Error: Don't have a process with this pid.Please check your input.")
            return
        else:
            parentPcb = desPcb.parent
            if parentPcb != None:       # 追溯到父进程 在子进程表中删除该进程
                parentPcb.childTree.remove(desPcb)
            self.__killPCB(desPcb)
        self.__scheduler()
    
    def __scheduler(self):
        if self.__readyList.__len__() == 0:
            print("Nothing is running.")
        else:
            for i in range(self.__maxPrio,-1,-1):
                for j in range(self.__readyList[i].__len__()):
                    self.__currentPoint = self.__readyList[i][j]
                    print("Process %s is running."%self.__readyList[i][j].pid)   # 返回就绪队列中最高优先级的第一个进程
                    return
            