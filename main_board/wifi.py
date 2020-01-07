import time
import network

class Wifi:
    def __init__(self, essid='Luo', password='22258926', output_fun=None):
        if output_fun is not None:
            self.print = output_fun.output
        else:
            self.print = print
        
        self.essid = essid
        self.password = password
        self.wifi = network.WLAN(network.STA_IF)
    
    def do_connect(self):
        self.wifi.active(True)
        if not self.wifi.isconnected():
            self.print('Conn to network...')
            self.wifi.connect(self.essid, self.password)
            flag = False
            for i in range(10):
                if self.wifi.isconnected():
                    flag = True
                    break
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
    # from machine import Pin
    # phase1A = Pin(26, Pin.IN, pull=Pin.PULL_UP)
    # phase1B = Pin(25, Pin.IN, pull=Pin.PULL_UP)
    # phase2A = Pin(35, Pin.IN, pull=Pin.PULL_UP)
    # phase2B = Pin(34, Pin.IN, pull=Pin.PULL_UP)
    # phase3A = Pin(27, Pin.IN, pull=Pin.PULL_UP)
    # phase3B = Pin(36, Pin.IN, pull=Pin.PULL_UP)

    # phase1A.irq(trigger=Pin.IRQ_FALLING, handler=lambda t:print("phase1A"))
    # phase1B.irq(trigger=Pin.IRQ_FALLING, handler=lambda t:print("phase1B"))
    # phase2A.irq(trigger=Pin.IRQ_FALLING, handler=lambda t:print("phase2A"))
    # phase2B.irq(trigger=Pin.IRQ_FALLING, handler=lambda t:print("phase2B"))
    # phase3A.irq(trigger=Pin.IRQ_FALLING, handler=lambda t:print("phase3A"))
    # phase3B.irq(trigger=Pin.IRQ_FALLING, handler=lambda t:print("phase3B"))
        
    wifi = Wifi()
    wifi.do_connect()
    # print(wifi.get_ip())
