# -*- coding: UTF-8 -*-

import socket
import time
import threading
import struct
from package import MsgID, PackageDict


SYNC_FLAG = 0xff

class Status:
    WAITING_SYNC_FLAG = 0
    RECEIVE_MSG_ID = 1
    RECEIVE_MSG_LEN_LOW = 2
    RECEIVE_MSG_LEN_HIGH = 3
    RECEIVE_PACKAGE = 4
    RECEIVE_CHECKSUM = 5

class Client:
    def __init__(self):
        self.status = Status.WAITING_SYNC_FLAG
        self.msg_id = 0
        self.msg_len = 0
        self.msg = bytearray()

        self.socket_client = socket.socket()         # 创建 socket 对象
        host = '192.168.50.122'     # esp32 ip
        port = 10000                # 设置端口号
        self.socket_client.connect((host, port))
        self.listen_run = True
        self.socket_listen = threading.Thread(target=self.listen)
        self.socket_listen.start()

    def __del__(self):
        self.listen_run = False
        self.socket_listen.join()

    def run(self):
        while True:
            msg = input('>>> ')
            msg_split = msg.split(",")
            msg_id = int(msg[0])
            param = None
            if msg_id == MsgID.ID_SET_MOTOR:
                param = list(map(int, msg_split[1:])) 
            data = self.make_command(msg_id, param)
            self.socket_client.send(data)
            time.sleep(0.5)

    def listen(self):
        while self.listen_run:
            data = self.socket_client.recv(1024)
            if not data:
                continue
            self.parse(data)
    
    def checksum(self, data):
        return 255 - sum(data) % 256

    def make_command(self, msg_id, param=None):
        pkg = PackageDict[msg_id].pack(param)
        data = struct.pack("<BH", msg_id, len(pkg)) + pkg
        return struct.pack("B", SYNC_FLAG) + data + struct.pack("B", self.checksum(data))

    def parse(self, buf):
        buf_len = len(buf)
        if buf_len == 0:
            return
        
        for i in range(buf_len):
            val = buf[i:i+1]
            if self.status is Status.WAITING_SYNC_FLAG:
                if ord(val) is SYNC_FLAG:
                    # print("WAITING_SYNC_FLAG")
                    self.msg_id = 0
                    self.msg_len = 0
                    self.data = bytearray()
                    self.package = bytearray()
                    self.status = Status.RECEIVE_MSG_ID
            
            elif self.status is Status.RECEIVE_MSG_ID:
                # print("RECEIVE_MSG_ID")
                self.data.extend(val)
                self.msg_id = ord(val)
                self.status = Status.RECEIVE_MSG_LEN_LOW
            
            elif self.status is Status.RECEIVE_MSG_LEN_LOW:
                # print("RECEIVE_MSG_LEN_LOW")
                self.data.extend(val)
                self.status = Status.RECEIVE_MSG_LEN_HIGH
                
            elif self.status is Status.RECEIVE_MSG_LEN_HIGH:
                # print("RECEIVE_MSG_LEN_HIGH")
                self.data.extend(val)
                self.msg_len, = struct.unpack("<H", self.data[-2:])
                if self.msg_len == 0:
                    self.status = Status.RECEIVE_CHECKSUM
                else:
                    self.status = Status.RECEIVE_PACKAGE
                # self.msg_len, = struct.unpack("<H", b''.join(self.msg[-2:]))
                # print(b''.join(self.msg[-2:]))
                
            elif self.status is Status.RECEIVE_PACKAGE:
                # print("RECEIVE_PACKAGE")
                self.package.extend(val)
                if len(self.package) == self.msg_len:
                    self.data.extend(self.package)
                    self.status = Status.RECEIVE_CHECKSUM
            
            elif self.status is Status.RECEIVE_CHECKSUM:
                # print("RECEIVE_CHECKSUM")
                self.status = Status.WAITING_SYNC_FLAG
                # print("checksum:", self.checksum(self.data))
                if ord(val) == self.checksum(self.data):
                    # print("Got a complete message.")
                    self.package_analysis()
            
            else:
                self.status = Status.WAITING_SYNC_FLAG

    def package_analysis(self):
        print("Get Msg ID:" + str(self.msg_id))
        pk = PackageDict[self.msg_id]
        if pk.unpack(self.package):
            print(pk.param)


if __name__ == '__main__':
    client = Client()
    client.run()

    # 1,2,0,2,0,2,0
    # 1,1,200,1,200,1,200
    # 1,0,200,0,200,0,200
    # print(msg)
    # print("send")
    # socket_client.send(b"motor,0,512,0,512,0,512")
    # time.sleep(1)