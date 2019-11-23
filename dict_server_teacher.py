''' 
name : Benson
data : 2019-11-22
email : lebronjb2437@gmail.com
modules : socket
This is a dict project for AID
'''


from socket import *
import os
import time
import signal
import pymysql
import sys

#定義需要的全局變量
DICT_TEXT = './dict.txt'
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)

#流程控制
def main():
    #創建數據庫連接
    db = pymysql.connect('localhost','root','a123456','dict')

    #創建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)
    #忽略子進程信號
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    while True:
        try:
            c,addr = s.accept()
            print("Connect from",addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit("服務端退出")
        except Exception as e:
            print(e)
            continue

        #創建子進程
        pid = os.fork()
        if pid == 0:
            s.close()
            
            do_child(c,db)
        else:
            c.close()
            continue

def do_child(c,db):
    #循環接收客戶端請求
    while True:
        data = c.recv(128).decode()
        print(c.getpeername(),":",data)
        if not data or data[0] == 'E':
            c.close()
            sys.exit(0)
        elif data[0] == 'R':
            do_register(c,db,data)
        elif data[0] == 'L':
            do_login(c,db,data)
        elif data[0] == 'Q':
            do_query(c,db,data)
        elif data[0] == 'H':
            do_history(c,db,data)

def do_register(c,db,data):
    print("註冊操作")
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    cursor = db.cursor()

    sql = "select * from user where name='%s'"%name
    cursor.execute(sql)
    r = cursor.fetchone()

    if r != None:
        c.send(b'EXISTS')
        return
    #用戶不存在插入用戶
    sql = "insert into user(name,passwd) values('%s','%s')"%(name,passwd)
    try:
        cursor.execute(sql)
        db.commit()
        c.send(b'OK')
    except:
        db.rollback()
        c.send(b'FAIL')
    else:
        print("%s註冊成功"%name)


def do_login(c,db,data):
    print("登入操作")
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    cursor = db.cursor()

    sql = "select * from user where name='%s' and passwd='%s'"%(name,passwd)
    cursor.execute(sql)
    r = cursor.fetchone()

    if r is None:
        c.send(b'FAIL')
    else:
        c.send(b'OK')
        print("%s登入成功"%name)
    
    

def do_query(c,db,data):
    print("查單詞操作")
    l = data.split(' ')
    name = l[1]
    word = l[2]
    cursor = db.cursor()

    sql = "select * from words where word='%s'"%word
    cursor.execute(sql)
    r = cursor.fetchone()
    if r is None:
        c.send(b'FAIL')
        print("數據庫沒有這個單詞")
    else:
        c.send(r[2].encode())
        print("%s查詢成功"%name)
    
        sql = "insert into history(name,word) values('%s','%s')"%(name,word)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()

def do_history(c,db,data):
    print("查歷史紀錄操作")
    l = data.split(' ')
    name = l[1]
    cursor = db.cursor()

    sql = "select word from history where name='%s'"%name
    cursor.execute(sql)
    r = cursor.fetchall()
    if r == ():
        c.send(b'None')
        print("尚未有%s查詢的紀錄"%name)
    else:
        i = ' '
        for word in r:
            i += word[0] + '#'
        c.send(i.encode())
        print("%s查詢歷史紀錄成功"%name)

    
    
if __name__ == "__main__":
    main()