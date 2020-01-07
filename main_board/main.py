from oled_print import OLEDPrint
from wifi import Wifi
from socket_server import SocketServer
from motor_control import MotorControl
from wheel_encoder import WheelEncoder
import global_params


if __name__ == '__main__':
    global_params.init()    
    global_params.set_value("motor_control", MotorControl())
    global_params.set_value("wheel_encoder", WheelEncoder())

    oled = OLEDPrint()
    wifi = Wifi(output_fun=oled)
    flag = wifi.do_connect()
    if flag is False:
        oled.output("Wifi Error")
        exit(0)
    ip = wifi.get_ip()

    socket_server = SocketServer(ip, output_fun=oled)
    socket_server.run()