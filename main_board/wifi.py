import network
import time

class Wifi:
    def __init__(self, essid='Luo', password='22258926', output_fun=None):
        if output_fun is not None:
            self.print = output_fun.output
        else:
            self.print = print
        
        self.essid = essid
        self.password = password
        self.wifi = network.WLAN(network.STA_IF)
        self.wifi.active(True)
    
    def do_connect(self):
        if not self.wifi.isconnected():
            self.print('Conn to network...')
            self.wifi.connect(self.essid, self.password)
            flag = False;
            for i in range(10):
                if self.wifi.isconnected():
                    flag = True;
                    break;
                else:
                    self.print('Wait for network...')
                    time.sleep(1)
        
            if flag is True:
                self.print('ESP32 IP:')
                self.print(self.wifi.ifconfig()[0])
            return flag
        else:
            self.print('ESP32 IP:')
            self.print(self.wifi.ifconfig()[0])
            return True
        
    def get_ip(self):
        return self.wifi.ifconfig()[0]

if __name__ == '__main__':
    wifi = Wifi()
    wifi.do_connect()
    print(wifi.get_ip())
