'''
Created on 2018年5月17日

@author: Murrey
'''
from Core import CoreManager

if __name__ == '__main__':
    coreManager =  CoreManager()
    while(True):
        message = input("Shell/murrey > ")
        message = message.split(' ')
        res = coreManager.decodeInstruction(message)
        if res == False:
            break
        