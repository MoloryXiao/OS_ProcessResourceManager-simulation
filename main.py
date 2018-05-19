'''
Created on 2018年5月17日

@author: Murrey
'''
if __name__ == '__main__':
    while(True):
        message = input("【输入指令】")
        if message == "cr":
            print("cr")
        elif message == "des":
            print("des")
        elif message == "break":
            break        
        print("输入内容为：%s"%message)
        