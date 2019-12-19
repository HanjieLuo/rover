"""
ESP32 pin
26 : Phase A, motor1
25 : Phase B, motor1
35 : Phase A, motor2
34 : Phase B, motor2
39 : Phase A, motor3
36 : Phase B, motor3
"""

from machine import Pin
import micropython
micropython.alloc_emergency_exception_buf(100)

class WheelEncoder:
    def __init__(self):        
        self.count1 = 0
        self.count2 = 0
        self.count3 = 0
        
        self.phase1A = Pin(26, Pin.IN, pull=Pin.PULL_UP)
        self.phase1B = Pin(25, Pin.IN, pull=Pin.PULL_UP)
        self.phase2A = Pin(35, Pin.IN, pull=Pin.PULL_UP)
        self.phase2B = Pin(34, Pin.IN, pull=Pin.PULL_UP)
        self.phase3A = Pin(39, Pin.IN, pull=Pin.PULL_UP)
        self.phase3B = Pin(36, Pin.IN, pull=Pin.PULL_UP)

        self.phase1A.irq(trigger=Pin.IRQ_FALLING, handler=self.irq_handler1)
        self.phase2A.irq(trigger=Pin.IRQ_FALLING, handler=self.irq_handler2)
        # self.phase3A.irq(trigger=Pin.IRQ_FALLING, handler=self.irq_handler3)
        
        # self.response1_ref = self.response1
        # self.response2_ref = self.response2
        # self.response3_ref = self.response3
        
    def irq_handler1(self, t):
        if(self.phase1B.value() == 1):
            self.count1 += 1
        else:
            self.count1 -= 1
        print("M1:", self.count1, " A:", self.phase1A.value(), " B:", self.phase1B.value())
        # micropython.schedule(self.response1_ref, 0)
    
    def irq_handler2(self, t):
        if(self.phase2B.value() == 1):
            self.count2 += 1
        else:
            self.count2 -= 1
        print("M2:", self.count2, " A:", self.phase2A.value(), " B:", self.phase2B.value())
        # micropython.schedule(self.response2_ref, 0)
    
    def irq_handler3(self, t):
        if(self.phase3B.value() == 1):
            self.count3 += 1
        else:
            self.count3 -= 1
        print("M3:", self.count3, " A:", self.phase3A.value(), " B:", self.phase3B.value())
        # micropython.schedule(self.response3_ref, 0)
    
    # def response1(self, _):
        # pass
    
    # def response2(self, _):
        # pass
    
    # def response3(self, _):
        # pass


if __name__ == '__main__':
    wheel_encoder = WheelEncoder()
    