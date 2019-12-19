# -*- coding: UTF-8 -*-

import socket
import time

socket_client = socket.socket()         # 创建 socket 对象
host = '192.168.50.122'     # esp32 ip
port = 10000                # 设置端口号

socket_client.connect((host, port))

while True:
	msg = input('>>> ')
	socket_client.send(msg.encode())
	# print(msg)
	# print("send")
	# socket_client.send(b"motor,0,512,0,512,0,512")
	# time.sleep(1)