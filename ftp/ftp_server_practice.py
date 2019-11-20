from socket import *
import os,sys
from time import sleep
import signal


FILE_PATH = '/home/ubuntu/ftp_file/'
HOST = '0.0.0.0'
PROT = 8000
ADDR = (HOST,PROT)


class FTPServer(object):
    def __init__(self,connfd):
        self.connfd = connfd

    def do_list(self):
        self.connfd.send('OK'.encode())
        sleep(0.1)    #防止粘包產生
        filelist = os.listdir(FILE_PATH)
        files = ''
        for file in filelist:
            if file[0] != '.' and os.path.isfile(FILE_PATH + file):
                files = files + file + '#'
       
        self.connfd.send(files.encode())





def main():
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    print("Listen the port 8000...")


    while True:
        try:
            connfd,addr = s.accept()
        except KeyboardInterrupt:
            s.close()
            sys.exit("服務端退出")
        except Exception as e:
            print("服務端異常",e)
            continue
        print("Connect from",addr)
        

        pid = os.fork()
        if pid == 0:
            s.close()
            ftp = FTPServer(connfd)
            while True:
                data = connfd.recv(1024).decode()
                if not data or data[0] == 'Q':
                    connfd.close()
                    sys.exit("客戶端退出")
                elif data[0] == 'L':
                    ftp.do_list()
              



        else:
            connfd.close()
            continue

if __name__ == "__main__":
    main()

