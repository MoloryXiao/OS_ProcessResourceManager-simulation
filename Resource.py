'''
Created on 2018年5月19日

@author: Murrey
'''
from RCB import NewRcb
from Item import *

class ResourceManager(object):
    def __init__(self,readyList):
        self.__readyList = readyList
        self.__blockingList = []
        self.__resourceList = []

    ####
    # 函数功能：根据提供的RID和资源数量num 创建一个资源并加入资源列表中
    ####
    def createResource(self,rid,num):
        if num == 0:
            return "ErrorNum"
        if self.getResource(rid) != False:
            return "ErrorRid"
        newRcb = NewRcb(rid,num)
        self.__resourceList.append(newRcb)
        return True
    
    ####
    # 函数功能：任务请求给定数量的资源
    ####
    def requestResource(self,pcb,rid,num):
        res = self.getResource(rid)
        
        if res == False:    # 判断资源是否存在
            return "ErrorRid"
        if res.sum < num:   # 判断资源申请数是否不超出资源本身最大值
            return "ErrorNum"
        
        # 合法申请或阻塞等待
        if res.available >= num: 
            # 若小于或等于，则创建资源使用块，加入该资源的使用队列中     
            usingItem = NewUsingListItem(pcb,num)   
            res.usingList.append(usingItem)
            res.available -= num
            rnResource = NewResourceItem(res.rid,num)            
            return rnResource   # 返回申请到的资源
        else:    
            # 创建等待块，加入该资源的等待队列
            # 创建阻塞块，加入资源管理器的阻塞队列
            # 返回阻塞标识        
            waitingItem = NewWaitingListItem(pcb,num)
            blockingItem = NewBlockingListItem(pcb,rid)
            res.waitingList.append(waitingItem)
            self.__blockingList.append(blockingItem)
            return "Blocking"
    
    ####   
    # 函数功能：进程释放给定数量的资源 并给定标志位标识是否执行唤醒操作
    ####
    def releaseResource(self,pcb,rid,releaseNum,isCheckWaitingList):
        res = self.getResource(rid)
        if res == False:    # 判断资源是否存在
            return "ErrorRid"
        if res.isPcbExistInUsingList(pcb) == False:    # 判断释放资源的进程是否在该资源下
            return "ErrorPid"
        
        item = res.getItemFromUsingList(pcb)
        if item.num < releaseNum:       # 判断是否非法释放
            return "ErrorReleaseNum"
        
        if res.available+releaseNum > res.sum: # 判断是否非法释放
            return "ErrorSum"
        
        res.modifyUsingList(pcb,releaseNum) # 修改资源中使用队列的情况
        pcb.modifyResourceNum(rid,(-1)*releaseNum) # 修改进程所持有的资源数量
        res.available += releaseNum    # 资源数量恢复
        
         
        if(isCheckWaitingList) : # 判断是否需要检查等待队列 如果单单释放资源则该位应为False
            # 检查阻塞队列  检查是否可进行资源分配      
            rnUsablePcbList = []
            while True:
                usableItem = res.findUsableWaitingItem() # 获得可用于进行分配操作的Item
                if usableItem == False: # 若没有可分配的Item 则跳出循环
                    break
                
                # 对Item进行一次分配操作
                getRes = self.requestResource(usableItem.pcb, res.rid, usableItem.num)
                # 检查pcb中是否已经拥有该资源块
                existResource = usableItem.pcb.findResource(getRes.rid)
                if existResource == False:
                    usableItem.pcb.resources.append(getRes) # 将获取到的资源加入该PCB的资源池中
                else:
                    existResource.num += getRes.num
                
                # 将该等待块记录从等待队列中移除
                res.waitingList.remove(res.getItemFromWaitingList(usableItem.pcb))
                # 将该阻塞块记录从阻塞队列中移除
                self.__blockingList.remove(self.getItemFromBlockingList(usableItem.pcb))
                # 将成功分配的pcb装入容器 等待返回后加入就绪队列
                rnUsablePcbList.append(usableItem.pcb)
            
            if rnUsablePcbList.__len__() == 0:
                return "Success"
            else:
                return rnUsablePcbList
        else:
            return "Success"
    
    ####
    #  函数功能：释放给定PCB列表中所有PCB的资源 并且不引起重新调度
    ####
    def releasePcbListResource(self,pcbList):
        # 释放所有进程所持有的资源 但不引起重新调度
        listLen = pcbList.__len__()
        for i in range(listLen):
            pcbTemp = pcbList[i]
            for j in range(pcbTemp.resources.__len__()):
                resTemp = pcbList[i].resources[j]
                self.releaseResource(pcbTemp, resTemp.rid, resTemp.num, False)
        
        # 对PCB列表中阻塞状态的PCB进行资源上的处理
        for i in range(listLen):
            pcbTemp = pcbList[i]
            if(pcbTemp.status == "blocking"):
                for j in range(self.__blockingList.__len__()):
                    if self.__blockingList[j].pcb == pcbTemp:
                        # 将其从该资源的等待队列中去除
                        resRid = self.__blockingList[j].rid
                        res = self.getResource(resRid)
                        res.deleItemFromWaitingList(pcbTemp)
                        # 将其从阻塞队列中去除
                        self.__blockingList.remove(self.__blockingList[j])
                        break
            else:
                continue
        return True

    ####
    # 函数功能：查看PCB是否存在于阻塞队列中 若存在则返回该阻塞项 
    ####
    def getItemFromBlockingList(self,pcb):
        for i in range(self.__blockingList.__len__()):
            if self.__blockingList[i].pcb == pcb:
                return self.__blockingList[i]
        return False
    
    ####
    # 函数功能：根据提供的RID 从资源列表中得到该资源 并返回
    ####
    def getResource(self,rid):
        listLen = self.__resourceList.__len__()
        for i in range(listLen):
            if self.__resourceList[i].rid == rid:
                return self.__resourceList[i]
        return False
    
    ####
    # 函数功能：打印所有资源的情况
    ####
    def printAllResource(self):
        listLen = self.__resourceList.__len__()
        print("\nResource Counts：%d"%listLen)
        print("==========ResourceList==========")
        for i in range(listLen):
            self.__resourceList[i].print()
        print("")
        
    ####
    # 函数功能：打印阻塞队列情况
    ####
    def printBlockingList(self):
        listLen = self.__blockingList.__len__()
        print("\nBlocking Item Counts：%d"%listLen)
        if listLen != 0:
            print("==========BlockingList==========")
            for i in range(listLen):
                self.__blockingList[i].print()
        print("")   # 换行