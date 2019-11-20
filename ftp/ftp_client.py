from socket import *
import sys,os
import time

#基本文件操作功能
class FtpClient(object):
    def __init__(self,sockfd):
        self.sockfd = sockfd

    def do_list(self):
        self.sockfd.send(b'L')  #發送請求
        #等待回覆
        data = self.sockfd.recv(1024).decode()
        if data == 'OK':
            data = self.sockfd.recv(4096).decode()
            files = data.split('#')
            for file in files:
                print(file)
            print("文件列表展示完畢\n")

        else:
            #由服務器發送失敗原因
            print(data)

    def do_get_file(self):
        file_name = input("請輸入要下載的文件名：")
        msg = 'G'+file_name
        self.sockfd.send(msg.encode())  #發送請求
        #等待回覆
        data = self.sockfd.recv(1024).decode()
        if data =="OK":
            file_name = input("請輸入要存儲的檔名:")
            data = self.sockfd.recv(4096).decode()
            f = open(file_name,'w')
            f.write(data)
            f.close()
            print("文件下載完畢")
        else:
            #由服務器發送失敗原因
            print(data)

    def do_put_file(self):
        filelist = os.listdir("/home/ubuntu/PythonThread/day4/ftp")
        for file in filelist:
    	    print(file)
        file_name = input("請輸入要上傳的文件名:")
        msg = 'P' + file_name
        self.sockfd.send(msg.encode())
        data = self.sockfd.recv(1024).decode()
        if data =="OK":
            f = open(file_name)
            data = f.read()
            self.sockfd.send(data.encode())
            f.close()
            data = self.sockfd.recv(4096).decode()
            print(data)
        else:
            print(data)



#網路連接
def main():
    if len(sys.argv) < 3:
        print("argv is error")
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)   #文件服務器地址

    sockfd = socket()
    try:
        sockfd.connect(ADDR)
    except:
        print("連接服務器失敗")
        return

    ftp = FtpClient(sockfd)   #功能類對象
    while True:
        print("==========命令選項============")
        print("***********list**************")
        print("**********get file***********")
        print("**********put file***********")
        print("************quit*************")
        print("=============================")

        cmd = input("請輸入命令>>")
        if cmd.strip() == "list":
            ftp.do_list()
        elif cmd.strip() == "get file":
            ftp.do_get_file()
        elif cmd.strip() == "put file":
            ftp.do_put_file()
        elif cmd.strip() == "quit":
            ftp.do_quit()


if __name__ == "__main__":
    main()