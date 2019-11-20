from socket import *
import os,sys
import signal

#客戶端處理函數
def client_handler(c):
    print("處理子進程的請求:",c.getpeername())
    try:
        while True:
            data = c.recv(1024)
            if not data:
                break
            print(data.decode())
            c.send("收到客戶端請求".encode())
    except (KeyboardInterrupt,SystemError):
        sys.exit("客戶端退出")
    except Exception as e:
        print(e)
    c.close()
    sys.exit(0)
    

#創建套接字
HOST = ""
PORT = 8888
ADDR = (HOST,PORT)

s = socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(ADDR)
s.listen(5)

print("進程%d等待客戶端連接"%os.getpid())

#在父進程中忽略子進程狀態改變，子進程退出自動由系統處理
signal.signal(signal.SIGCHLD,signal.SIG_IGN)

while True:
    try:
        c,addr = s.accept()
    except KeyboardInterrupt:
        sys.exit("服務器退出")
    except Exception as e:
        print("Error:",e)
        continue

    #位客戶端創建新的進程處理請求
    pid = os.fork()
    #子進程處理具體請求
    if pid == 0:
        s.close()
        client_handler(c)
    
    #父進程或者創建失敗都繼續等待下個客戶端連接
    else:
        c.close()
        continue


