'''
Created on 2018年5月19日

@author: Murrey
'''
from PCB import NewPCB

class ProcessManager(object):
    __maxPrio = 2
    __currentPoint = None
    __pcbList = []
    
    def __init__(self,readyList):
        self.__readyList = readyList
        initPcb = NewPCB("init",0,"ready")
        self.__readyList[0].append(initPcb)    # 将新进程加入对应的就绪队列
        self.__scheduler()    # 进程调度
    
    ####
    # 函数功能：创建一个进程
    ####
    def createProcess(self,pid,prio):
        if self.getProcess(pid) != False:
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
        self.__pcbList.append(newPcb)
        self.__scheduler()    # 进程调度
    
    ####
    # 函数功能：销毁一个进程 与killPCB合作实现
    ####
    def destoryProcess(self,pid):
        desPcb = self.getProcess(pid)
        if desPcb == None:
            print("Error: Don't have a process with this pid.Please check your input.")
            return
        else:
            parentPcb = desPcb.parent
            if parentPcb != None:       # 追溯到父进程 在子进程表中删除该进程
                parentPcb.childTree.remove(desPcb)
            self.__killPCB(desPcb)
        self.__scheduler()


    ####
    # 函数功能：kill相关进程及其子进程 前提是所有进程均在就绪队列中
    ####
    def __killPCB(self,pcb):
        childNum = pcb.childTree.__len__()
        l_prio = pcb.prio
        if childNum == 0:            
            self.__readyList[l_prio].remove(pcb)
            self.__pcbList.remove(pcb)
        else:
            for i in range(childNum):
                self.__killPCB(pcb.childTree[i])
            self.__readyList[l_prio].remove(pcb)
            self.__pcbList.remove(pcb)
            
    ####
    # 函数功能：超时重新调度
    ####
    def timeOut(self):
        desPcb = self.__currentPoint
        if desPcb.prio == 0:
            print("Warning: Current Process is <init>. Can not be switched.")
            return
        self.__readyList[desPcb.prio].remove(desPcb) # 移除出队列
        self.__readyList[desPcb.prio].append(desPcb) # 加到队尾
        self.__scheduler()
        
    ####
    # 函数功能：资源请求阻塞
    ####
    def resRequestBlock(self):
        self.__currentPoint.status = "blocking"
        lprio = self.__currentPoint.prio
        self.__readyList[lprio].remove(self.__currentPoint)    
        self.__currentPoint = None # 当前指向变为空    
        self.__scheduler()
        
    ####
    # 函数功能：资源请求成功
    ####
    def resRequestSuccess(self,resReq):
        getRes = self.__currentPoint.findResource(resReq.rid)
        if getRes == False:
            self.__currentPoint.resources.append(resReq)
        else:
            getRes.num += resReq.num
    
    ####
    # 函数功能：让PCB列表中的阻塞PCB重新加入就绪队列
    ####
    def letBlockPcbReturnReadyList(self,pcbList):
        listNew = []
        for i in range(pcbList.__len__()):
            if pcbList[i].status == "blocking":
                listNew.append(pcbList[i])
        self.anyPcbInReadyList(listNew, False)
    
    ####
    # 函数功能：将若干进程加入就绪队列 需要 标识是否需要重新调度
    ####
    def anyPcbInReadyList(self,pcbList,isReschedule):
        for i in range(pcbList.__len__()):
            pcbList[i].status = "ready"
            self.__readyList[pcbList[i].prio].append(pcbList[i])
        if isReschedule:
            self.__scheduler()    
            
    ####
    # 函数功能：调度
    ####
    def __scheduler(self):
        if self.__countReadyPCB() == 0:
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
                    else:   # 若最高优先级进程与当前进程一致
                        print("Process %s is running."%self.__currentPoint.pid)
                        return

    ####
    # 函数功能：获取当前进程
    ####
    def getCurrentPcbPoint(self):
        return self.__currentPoint
    
    ####
    # 函数功能：根据给定PID 返回对应的进程对象
    ####
    def getProcess(self,pid):
        for i in range(self.__pcbList.__len__()):
            if self.__pcbList[i].pid == pid:
                return self.__pcbList[i]            
        return False
    
    ####
    # 函数功能：获取PCB的子树 包括本身
    ####
    def getChildTreeAllPcb(self,pid,pcbList):
        pcb = self.getProcess(pid)
        
        if pcb.childTree.__len__() == 0:
            pcbList.append(pcb)
            return
        for i in range(pcb.childTree.__len__()):
            self.getChildTreeAllPcb(pcb.childTree[i].pid,pcbList)
        pcbList.append(pcb)
        
        return
            
    ####
    # 函数功能：统计已就绪的PCB数量
    ####
    def __countReadyPCB(self):
        count =0
        for i in range(self.__readyList.__len__()):
            count += self.__readyList[i].__len__()
        return count
    
    ####
    # 函数功能：打印所有PCB信息
    ####
    def printAllPcbList(self):
        listLen = self.__pcbList.__len__()
        print("\nPCB Counts：%d"%listLen)
        print("==========PCB_List==========")
        for i in range(listLen):
            self.__pcbList[i].print()
        print("")

    ####
    # 函数功能：打印就绪队列
    ####
    def printReadyList(self):
        print("\nProecess Counts：%d"%self.__countReadyPCB())
        for i in range(self. __maxPrio,-1,-1):
            print("==========ReadyList_%d=========="%i)
            for j in range(self.__readyList[i].__len__()):
                self.__readyList[i][j].print()
        print("")