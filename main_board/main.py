from oled_print import OLEDPrint
from wifi import Wifi
from socket_server import SocketServer


if __name__ == '__main__':
    pass
    # oled = OLEDPrint()
    
    # wifi = Wifi(output_fun=oled)
    # flag = wifi.do_connect()
    # if flag is False:
    #     exit(0)
    # ip = wifi.get_ip()

#     socket_server = SocketServer(ip, output_fun=oled)
#     socket_server.run()