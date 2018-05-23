'''
Created on 2018年5月17日

@author: Murrey
'''
from Core import CoreManager

if __name__ == '__main__':
    coreMan =  CoreManager()
    while(True):
        message = input("*** Please input your command：")
        message = message.split(' ')
        res = coreMan.decodeInstruction(message)
        if res == False:
            break
        