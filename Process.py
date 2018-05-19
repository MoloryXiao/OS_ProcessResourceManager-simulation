'''
Created on 2018年5月19日

@author: Murrey
'''
from PCB import NewPCB
class ProcessManager(object):
    __currentPoint = 0
    __maxPrio = 2
    __readyList = [ [] for i in range(3) ]
    __blockList = []
    def __init__(self, params):
        self.t = params
    
    def createProcess(self,name,prio):
        if prio > self.__maxPrio:       # 优先级越界
            print("Error: create process error.Priority is illegal.")
            
        newPcb = NewPCB(name,prio)
        if self.__currentPoint == 0:    # 第一进程
            self.__currentPoint = newPcb
        else:
            self.__currentPoint.childTree.append(newPcb)    # 将新进程与当前进程进行关联
            self.__readyList[prio].append(newPcb)    # 将新进程加入对应的就绪队列
        return self.__readyList[self.__maxPrio][0]   # 返回就绪队列中最高优先级的第一个进程