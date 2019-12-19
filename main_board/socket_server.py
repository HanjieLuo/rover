from motor_control import MotorControl
import time
import socket

class SocketServer:
    def __init__(self, ip, port=10000, output_fun=None):
        self.motor_control = MotorControl()
        
        self.listen_socket = socket.socket()   #创建套接字
        self.listen_socket.bind((ip, port))   #绑定地址和端口号
        self.listen_socket.listen(1)   #监听套接字, 最多允许一个连接
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   #设置套接字
        
        if output_fun is not None:
            self.print = output_fun.output
        else:
            self.print = print
        self.print ('Sck waiting...')
            
    def run(self):
        try:
            while True:
                self.print("Sck accepting...")
                conn, addr = self.listen_socket.accept()   #接收连接请求，返回收发数据的套接字对象和客户端地址
                self.print ("Conn by:")
                self.print (addr[0])
                
                while True:
                    data = conn.recv(1024)   #接收数据（1024字节大小）
                    if(len(data) == 0):   #判断客户端是否断开连接
                        self.print("Close Sck")
                        conn.close()   #关闭套接字
                        break
                    else:
                        self.anaylse(data)
        except:
            if(self.listen_socket):   #判断套接字是否为空
                self.listen_socket.close()   #关闭套接字
                self.print("Sck exit")
    
    def anaylse(self, input_data):
        data = input_data.decode("utf-8")
        self.print("Rx:" + data)
        words = data.split(',')
        if words[0] is "motor":
            if len(words) is not 7:
                return
            self.motor_control.control(int(words[1]), int(words[2]), int(words[3]), int(words[4]), int(words[5]), int(words[6]))
        elif words[0] is "stop":
            self.listen_socket.close()   #关闭套接字
            raise Exception("Exit")

if __name__ == '__main__':
    from oled_print import OLEDPrint
    from wifi import Wifi
    
    output = OLEDPrint()
#     output = None
    
    wifi = Wifi(output_fun=output)
    flag = wifi.do_connect()
    if flag is False:
        exit(0)
    ip = wifi.get_ip()

    socket_server = SocketServer(ip, output_fun=output)
    socket_server.run()

