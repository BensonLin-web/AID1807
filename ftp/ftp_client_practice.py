from socket import *
import signal
import time
import os,sys




class FTPClient(object):
    def __init__(self,sockfd):
        self.sockfd = sockfd

    def do_list(self):
        self.sockfd.send("L".encode())
        data = self.sockfd.recv(1024).decode()
        if data == 'OK':
            data = self.sockfd.recv(1024).decode()
                
            file_list = data.split('#')
            for filename in file_list:
                print(filename)
            print("文件展示完畢\n")
        else:
            print(data)  #打印服務端錯誤信息
            return







def main():
    if len(sys.argv) < 3:
        print("未輸入IP或端口")
        return

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)
    sockfd = socket()
    try:
        sockfd.connect(ADDR)
    except:
        print("服務端連接失敗")
        return
    ftp = FTPClient(sockfd)
    while True:
        print("=========命令清單===========")
        print("========show list==========")
        print("========get file===========")
        print("========put file===========")
        print("==========quit=============")
        try:
            cmd = input("請輸入指令：")
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit("客戶端退出")
        except Exception as e:
            print("Error:",e)
            continue
        if cmd.strip() == "show list":
            ftp.do_list()


if __name__ == "__main__":
    main()
