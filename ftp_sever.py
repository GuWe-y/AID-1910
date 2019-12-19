"""
ftp文件处理
env ：python3.6
多线程并发 & socket
"""
from threading import Thread
from socket import *
import sys,signal,os
import time
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST,PORT)
FTP = '/home/tarena/FTP/'
#实现文件传输的具体功能
class FTPSever(Thread):
    def __init__(self,connfd):
        super().__init__()
        self.connfd = connfd
    #处理文件列表发送
    def do_list(self):
        # 获取文件列表
        file_list = os.listdir(FTP)
        if not file_list:
            self.connfd.send('文件库为空'.encode())
            return
        else:
            self.connfd.send(b'OK')
            time.sleep(0.1)
        #发送文件列表
        files = '\n'.join(file_list)
        self.connfd.send(files.encode())
 # 文件下载
    def do_retr(self,filename):
        try:
            f = open(FTP + filename,'rb')
        except Exception:
            self.connfd.send('文件不存在'.encode())
            return
        else:
            self.connfd.send(b'OK')
            time.sleep(0.1)

        while True:
            data = f.read(1024)
            if not data:
                time.sleep(0.1)
                self.connfd.send(b"##")
                break
            self.connfd.send(data)
        f.close()
    #处理上传文件
    def do_stor(self,filename):
        if os.path.exists(FTP + filename):
            self.connfd.send("文件已存在".encode())
            return

        else:
            self.connfd.send(b'OK')
        #接收文件
        f = open(FTP+filename,'wb')
        while True:
            data = self.connfd.recv(1024)
            if data ==b'##':
            #文件发送完
                break
            f.write(data)
        f.close()
    def run(self):
        while True:
            data = self.connfd.recv(1024).decode()
            if data == 'LIST':
                print(data)
            elif data == 'QUIT':
                pass
#搭建网络模型
def main():
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(3)

    print("OK 8888...")
    while True:
        try:
            c, addr = s.accept()
            print("connect from", addr)
        except KeyboardInterrupt:
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue
        # 创建线程
        t = FTPSever(c)
        t.setDaemon(True)  # 主线程退出其他线程也退出
        t.start()

if __name__ == '__main__':
    main()