"""
pin
22: scl
21: sda 
"""
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

class OLEDPrint:
    def __init__(self, i2c=None, addr=60, row_height=10, width=128, height=64):
        if i2c is None:
            i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
        
        # All characters have dimensions of 8x8 pixels and there is currently no way to change the font.
        self.width = width
        self.height = height
        self.row_height = row_height
        self.row_max = height - row_height 
        self.row_idx = 0
        self.range = range(self.row_height)
        # self.scroll_step = - height % row_height

        self.oled = SSD1306_I2C(width, height, i2c, addr=addr)
        self.oled.fill(0)
        self.oled.show()
    
    def output(self, text):
        if self.row_idx > self.row_max:
            for i in self.range:
                self.oled.scroll(0, -1)
            self.row_idx -= self.row_height

        self.oled.text(str(text), 0, self.row_idx)
        self.row_idx += self.row_height
        self.oled.show()

if __name__ == '__main__':
    import time
    
    print_text = OLEDPrint()
    print_text.output("1")
    time.sleep(0.5)
    print_text.output("2")
    time.sleep(0.5)
    print_text.output("3")
    time.sleep(0.5)
    print_text.output("4")
    time.sleep(0.5)
    print_text.output("5")
    time.sleep(0.5)
    print_text.output("6")
    time.sleep(0.5)
    print_text.output("7")
    time.sleep(0.5)
    print_text.output("8")
    time.sleep(0.5)
    print_text.output("9")
    time.sleep(0.5)
    print_text.output("10")
    time.sleep(0.5)
    print_text.output("11")
    time.sleep(0.5)
    print_text.output("12")
    time.sleep(0.5)
