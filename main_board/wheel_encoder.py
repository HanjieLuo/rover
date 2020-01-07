from machine import Pin
import machine
from machine import Timer
import micropython
import utime
import math

micropython.alloc_emergency_exception_buf(100)

"""
ESP32 pin
26 : Phase A, motor1
25 : Phase B, motor1
35 : Phase A, motor2
34 : Phase B, motor2
27 : Phase A, motor3
36 : Phase B, motor3
"""

"""
Motor
390 pulse per circle
"""

# count1 = 0

# def irq_handler1(t):
#     micropython.schedule(response1, 0)
    
# def response1(_):
#     global count1
#     count1 += 1
#     print(count1)
    
# pulse_per_circle=390
# speed1 = 0.0
        
# rad_per_pulse = 2 * math.pi / pulse_per_circle

# phase1A = Pin(26, Pin.IN, pull=Pin.PULL_UP)
# phase1B = Pin(25, Pin.IN, pull=Pin.PULL_UP)

# phase1A.irq(trigger=Pin.IRQ_FALLING, handler=irq_handler1)

class WheelEncoder:
    def __init__(self, pulse_per_circle=390):
        # print("WheelEncoder")
        self.pulse_per_circle = pulse_per_circle
                
        self.count1 = 0
        self.count2 = 0
        self.count3 = 0
        
        self.pre_count1 = 0
        self.pre_count2 = 0
        self.pre_count3 = 0
        
        self.speed1 = 0.0
        self.speed2 = 0.0
        self.speed3 = 0.0
                
        self.rad_per_pulse = 2 * math.pi / pulse_per_circle
        
        self.phase1A = Pin(26, Pin.IN, pull=Pin.PULL_UP)
        self.phase1B = Pin(25, Pin.IN, pull=Pin.PULL_UP)
        self.phase2A = Pin(35, Pin.IN, pull=Pin.PULL_UP)
        self.phase2B = Pin(34, Pin.IN, pull=Pin.PULL_UP)
        self.phase3A = Pin(27, Pin.IN, pull=Pin.PULL_UP)
        self.phase3B = Pin(36, Pin.IN, pull=Pin.PULL_UP)

        self.phase1A.irq(trigger=Pin.IRQ_FALLING, handler=self.irq_handler1)
        self.phase2A.irq(trigger=Pin.IRQ_FALLING, handler=self.irq_handler2)
        self.phase3A.irq(trigger=Pin.IRQ_FALLING, handler=self.irq_handler3)
        
        # self.response1_ref = self.response1
        
        self.timer = Timer(1)
        self.period = 0.25 # 0.5s
        self.timer.init(period=int(self.period*1000), mode=Timer.PERIODIC, callback=self.caculate_speed) # 500ms
            
    def irq_handler1(self, t):
        # micropython.schedule(self.response1_ref, 0)
        self.count1 += 1 if (self.phase1B.value() == 1) else -1
        # print(self.count1)
    
    def irq_handler2(self, t):
        self.count2 += 1 if (self.phase2B.value() == 1) else -1
        # print(self.count2)
    
    def irq_handler3(self, t):
        self.count3 += 1 if (self.phase3B.value() == 1) else -1
        # print(self.count3)

    def response1(self, _):
        self.count1 += 1 if (self.phase1B.value() == 1) else -1
        # print(self.count1)
        
    def caculate_speed(self, t):
        irq_state = machine.disable_irq() # Start of critical section
                
        self.speed1 = (self.count1 - self.pre_count1) * self.rad_per_pulse * 2
        self.speed2 = (self.count2 - self.pre_count2) * self.rad_per_pulse * 2
        self.speed3 = (self.count3 - self.pre_count3) * self.rad_per_pulse * 2
        
        self.pre_count1 = self.count1
        self.pre_count2 = self.count2
        self.pre_count3 = self.count3
        
        machine.enable_irq(irq_state) # End of critical section
    
    def get_status(self):
        return self.count1, self.count2, self.count3, self.speed1, self.speed2, self.speed3
    
    def reset(self):
        self.count1 = 0
        self.count2 = 0
        self.count3 = 0
        
        self.pre_count1 = 0
        self.pre_count2 = 0
        self.pre_count3 = 0
        
        self.speed1 = 0.0
        self.speed2 = 0.0
        self.speed3 = 0.0


if __name__ == '__main__':
    wheel_encoder = WheelEncoder()
    while True:
        [rot1, rot2, rot3, v_rot1, v_rot2, v_rot3] = wheel_encoder.get_status()
        print(rot1, rot2, rot3, v_rot1, v_rot2, v_rot3)
        utime.sleep(1)
    