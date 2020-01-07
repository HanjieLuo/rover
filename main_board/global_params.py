from oled_print import OLEDPrint
from motor_control import MotorControl
from wheel_encoder import WheelEncoder

def init():
    global dict
    dict = {}
        
def set_value(key, value):
    dict[key] = value

def get_value(key, defValue=None):
    try:
        return dict[key]
    except KeyError:
        return defValue

if __name__ == '__main__':
    init()
    set_value("oled", OLEDPrint())
    
    oled = get_value("oled")
    oled.output("ok")
