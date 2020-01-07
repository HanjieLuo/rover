from machine import Pin, PWM
from shift_register import ShiftRegister

"""
595 pin
1 : INB, motor3
2 : INA, motor3
3 : INB, motor2
4 : INA, motor2
5 :
6 : INB, motor1
7 : INA, motor1

ESP32 pin
4 : PWM, motor1
0 : PWM, motor2
2 : PWM, motor3
"""

class MotorControl:
    def __init__(self):
        self.sr = ShiftRegister()
        #[Q8(7) Q7(6) Q6(5) Q5(4) Q4(3) Q3(2) Q2(1) Q1(15)]
        self.buf = bytearray([0b00000000])
        self.sr.send(self.buf)
        
        # 频率须位于1Hz和78125Hz
        # 占空比介于0至1023间，其中512为50%。
        self.pwm_m1 = PWM(Pin(4), freq=17000, duty=0)
        self.pwm_m2 = PWM(Pin(0), freq=17000, duty=0)
        self.pwm_m3 = PWM(Pin(2), freq=17000, duty=0)
        
        # 正，反，停
        self.dir = [[0b01000000, 0b10000000, 0b00000000], [0b00001000, 0b00010000, 0b00000000], [0b00000010, 0b00000100, 0b00000000]]
        
        self.dir_params = [0, 1, 2]
        self.speed_params = range(0, 1024)
    
    def control(self, dir1, speed1, dir2, speed2, dir3, speed3):
        if dir1 in self.dir_params and\
           dir2 in self.dir_params and\
           dir3 in self.dir_params and\
           speed1 in self.speed_params and\
           speed2 in self.speed_params and\
           speed3 in self.speed_params:
            self.buf[0] = self.dir[0][dir1] | self.dir[1][dir2] | self.dir[2][dir3]
            self.sr.send(self.buf)
        
            self.pwm_m1.duty(speed1)
            self.pwm_m2.duty(speed2)
            self.pwm_m3.duty(speed3)
        
if __name__ == '__main__':
    motor_control = MotorControl()
    motor_control.control(0, 512, 0, 512, 0, 512)
    
#     motor_control = MotorControl()
#     motor_control.control(0, 512, 0, 512, 0, 512)
#     print("motor")
#     sr = ShiftRegister()
#     buf = bytearray([0b10101010])
#     for i in range (1):
#         sr.send(buf)
#         print("send")
#         utime.sleep_ms(1000)