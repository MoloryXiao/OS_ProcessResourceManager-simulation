'''
Created on 2018年5月23日

@author: Murrey
'''
from Process import ProcessManager
from Resource import ResourceManager

MAX_PRIORITY = 3

class CoreManager(object):
    __readyList = [ [] for i in range(MAX_PRIORITY) ]    
    
    def __init__(self):
        self.__procManager = ProcessManager(self.__readyList)
        self.__resManager = ResourceManager(self.__readyList)
        
        # 测试用
        self.__resManager.createResource("R1", 1)
        self.__resManager.createResource("R2", 2)
        self.__resManager.createResource("R3", 3)
        self.__resManager.createResource("R4", 4)
        self.__resManager.createResource("R5", 5)
        # 测试用
    
    # 解码输入的命令
    def decodeInstruction(self,message):
        paramsCount = message.__len__()     
        if message[0] == "cr" and paramsCount == 3:
            self.createProcess(message)
        elif message[0] == "res" and paramsCount == 3:
            self.createResource(message)
        elif message[0] == "de" and paramsCount == 2:
            self.destoryProcess(message)
        elif message[0] == "list" and paramsCount == 2:
            self.printInfo(message)
        elif message[0] == "req" and paramsCount == 3:
            self.requestRes(message)
        elif message[0] == "rel" and paramsCount == 3:
            self.releaseRes(message)
        elif message[0] == "to" and paramsCount == 1:
            self.timeout()
        elif message[0] == "current" and paramsCount == 1:
            print("Process %s is running."%self.__procManager.getCurrentPcbPoint().pid)
#         elif message[0] == "debug":
#             self.debug(message)
        elif message[0] == "break":
            return False
        else:
            print("Please check your command.")
        return True    
    
    # 创建新进程
    def createProcess(self,message):
        pid = message[1]
        prio = int(message[2])
        self.__procManager.createProcess(pid, prio)
        
    # 创建新资源
    def createResource(self,message):
        rid = message[1]
        num = int(message[2])
        self.__resManager.createResource(rid, num)
    
    # 销毁进程
    def destoryProcess(self,message):
        pid = message[1]
        if self.__procManager.getProcess(pid) == False:
            print("Error: the pcb with %s doesn't exist."%pid)
            return
        pcbList = []
        self.__procManager.getChildTreeAllPcb(pid, pcbList) # 获取该进程子树 包括该进程
        self.__resManager.releasePcbListResource(pcbList) # 释放资源
        self.__procManager.letBlockPcbReturnReadyList(pcbList) # 让阻塞的Pcb回到就绪队列中
        self.__procManager.destoryProcess(pid)
    
    # 打印相关资源
    def printInfo(self,message):
        if message[1] == "Proc":
            self.__procManager.printReadyList()
        elif message[1] == "Res":
            self.__resManager.printAllResource()
        elif message[1] == "Block":
            self.__resManager.printBlockingList()
        elif message[1] == "Pcb":
            self.__procManager.printAllPcbList()
        elif message[1] == "--help":
            print("=====================================")
            print("list Proc: to get the list of all process in the readyList.")
            print("list Res: to get the list of all resouces in the resourceList.")
            print("=====================================")
        else:
            print("Please check your command.")
        
    # 时间片轮转
    def timeout(self):
        self.__procManager.timeOut()
        
    # 请求资源
    def requestRes(self,message):
        rid = message[1]
        num = int(message[2])
        resourceReq = self.__resManager.requestResource(self.__procManager.getCurrentPcbPoint(), rid, num)
        if resourceReq == "ErrorRid":
            print("Error: Could not find the resource with rid=%s, please check your input."%rid)
        elif resourceReq == "ErrorNum":
            print("Error: the number of resource requested is more than its possession.")
        elif resourceReq == "Blocking":
            print("Current process is blocking.")
            self.__procManager.resRequestBlock()
        else:
            print("Success: num=%d rid=%s are allocated to the process with pid=%s"
                  %(num,rid,self.__procManager.getCurrentPcbPoint().pid))
            self.__procManager.resRequestSuccess(resourceReq)
            
    def releaseRes(self,message):
        rid = message[1]
        releaseNum = int(message[2])
        rnResult = self.__resManager.releaseResource(self.__procManager.getCurrentPcbPoint(), rid, releaseNum,True)
        if rnResult == "ErrorRid":
            print("Error: can not release the resource with the valid rid.")
        elif rnResult == "ErrorPid":
            print("Error: Resource=%s's usingList do not include current PCB"%rid)
        elif rnResult == "ErrorReleaseNum":
            print("Error: ReleaseNum error.")
        elif rnResult == "ErrorSum":
            print("Error: ResourceSum error.")
        elif rnResult == "Success":
            print("Success: Release resource --- OK")
            pass
        else: # 将唤醒的进程加入就绪队列 并重新进行调度
            self.__procManager.anyPcbInReadyList(rnResult,True)
            
            
            
            
            
            
            