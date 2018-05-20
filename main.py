'''
Created on 2018年5月17日

@author: Murrey
'''
from Process import ProcessManager
from PCB import NewPCB

if __name__ == '__main__':
    procManager = ProcessManager()
    while(True):
        message = input("【Please input your command】")
        message = message.split(' ')
        if message[0] == "cr":
            l_pid = message[1]
            l_prio = int(message[2])
            procManager.createProcess(l_pid, l_prio)
        elif message[0] == "de":
            l_pid = message[1]
            procManager.destoryProcess(l_pid)
        elif message[0] == "list":
            procManager.printReadyList()
        elif message[0] == "break":
            break
        else:
            print("Please check your command.")
        