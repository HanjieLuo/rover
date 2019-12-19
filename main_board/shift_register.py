# exercise SPI with a 74HC595 shift register connected:
"""
pin
16      : VCC
15      : not connected
14   SER: GPIO23  MOSI(Serial Data In)
13    OE: GND (Output Enable)
12  RCLK: GPIO5 SS
11 SRCLK: GPIO18 SCK (latch)
10 SRCLR: VCC
9       : not connected
"""

from machine import Pin, SPI

class ShiftRegister:
    def __init__(self, rclk=5):
        # construct an SPI bus on the given pins
        # polarity is the idle state of SCK
        # phase=0 means sample on the first edge of SCK, phase=1 means the second
        self.vspi = SPI(2, baudrate=100000, polarity=0, phase=0, bits=8, firstbit=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
        self.rckl = Pin(rclk, mode=Pin.OUT, value=0)
    
    def send(self, buf):
        self.vspi.write(buf)
        self.rckl.value(1)
        self.rckl.value(0)

