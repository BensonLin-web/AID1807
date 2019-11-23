#!/usr/bin/python3
#coding=utf8

from socket import *
import sys
import getpass

#創建網路連接
def main():
    if len(sys.argv) < 3:
        print("argv is error")
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)

    s = socket()
    try:
        s.connect(ADDR)
    except Exception as e:
        print(e)
        return
    while True:
        print('''
        	=====================Welcome===================
        	--    1.註冊          2.登入        3.退出    --
        	===============================================
        	''')
        try:
            cmd = int(input("請輸入選項>>"))
        except Exception as e:
            print("命令錯誤")
            continue

        if cmd not in [1,2,3]:
            print("請輸入正確選項")
            sys.stdin.flush()  #清除標準輸入
            continue
        if cmd == 1:
            name = do_register(s)
            if name == 1:
                print("用戶存在")
            elif name ==2:
                print("註冊失敗")
            else:
                print("註冊成功")
                do_second_page(s,name)
            
        elif cmd == 2:
            name = do_login(s)
            if name :
                print("登入成功")
                do_second_page(s,name)
            else:
                print("用戶名或密碼有誤！")
        elif cmd == 3:
            s.send(b'E')
            sys.exit("謝謝使用")
        

def do_register(s):
    while True:
        name = input("User:")
        passwd = getpass.getpass()
        passwd1 = getpass.getpass('Again:')

        if (' ' in name) or (' ' in passwd):
            print("用戶和密碼不許有空格")
            continue
        if passwd != passwd1:
            print("兩次密碼不一樣")
            continue
        msg = 'R {} {}'.format(name,passwd)
        #發送請求
        s.send(msg.encode())
        #等待回覆
        data = s.recv(128).decode()
        if data == 'OK':
            return name
        elif data == 'EXISTS':
            return 1
        else:
            return 2
          
           
def do_login(s):
    name = input("User：")
    passwd = getpass.getpass()
    msg = 'L {} {}'.format(name,passwd)
    s.send(msg.encode())
    data = s.recv(128).decode()

    if data == 'OK':
        return name
    else:
        return 
       
    

def do_second_page(s,name):
    while True:
        print('''  
        	     =====================查詢界面===================
        	     --    1.查單詞      2.查看歷史紀錄        3.退出 --
        	     ===============================================
        	''')
        try:
            cmd = int(input("請輸入選項>>"))
        except Exception as e:
            print("命令錯誤")
            continue

        if cmd not in [1,2,3]:
            print("請輸入正確選項")
            sys.stdin.flush()  #清除標準輸入
            continue

        elif cmd ==1:
            data = do_query(s,name)
            if data == 0:
                print("您查詢的單詞不存在")
            else:
                print("解釋：",data)
        elif cmd ==2:
            data = do_history(s,name)
            if data == 0:
                print("尚未有您的查詢歷史紀錄")
            else:
                hist_list = data.split('#')
                print("您的歷史單詞查詢紀錄為：",end = '')
                for hist_word in hist_list:
                    print(hist_word,end = '   ')
                print()
        elif cmd ==3:
            return

def do_query(s,name):
    word = input("請輸入單詞：")
    msg = 'Q {} {}'.format(name,word)
    s.send(msg.encode())
    data = s.recv(1024).decode()
    if data == 'FAIL':
        return 0
    else:
        return data

def do_history(s,name):
    msg = 'H {}'.format(name)
    s.send(msg.encode())
    data = s.recv(1024).decode()
    if data == 'None':
        return 0
    else:
        return data

    




if __name__ == "__main__":
    main()