import struct
import global_params
# from motor_control import MotorControl
# from wheel_encoder import WheelEncoder

# motor_control = MotorControl()
# wheel_encoder = WheelEncoder()

class MsgID:
    ID_SET_MOTOR = 1
    ID_GET_MOTOR = 2
 
class Package:
    def pack(self, param=None):
        return b''

    def unpack(self, data):
        return True   

class PackageSetMotor(Package):
    def __init__(self):
        self.need_response = False
        # [dir1, speed1, dir2, speed2, dir3, speed3]
        self.param = [2, 0, 2, 0, 2, 0]

    def pack(self, param=None):
        if param is None:
            return struct.pack('6H', self.param[0], self.param[1], self.param[2], self.param[3], self.param[4], self.param[5])
        return struct.pack('6H', param[0], param[1], param[2], param[3], param[4], param[5])

    def unpack(self, data):
        try:
            self.param = struct.unpack('6H', data)
        except:
            return False
        global_params.get_value("motor_control").control(self.param[0], self.param[1], self.param[2], self.param[3], self.param[4], self.param[5])
        return True
    
class PackageGetMotor(Package):
    def __init__(self):
        self.need_response = True
        self.param = [0, 0, 0, 0.0, 0.0, 0.0]

    def pack(self, param=None):
        if param is None:
            self.param = global_params.get_value("wheel_encoder").get_status()
            return struct.pack('3i3f', self.param[0], self.param[1], self.param[2], self.param[3], self.param[4], self.param[5])
        return struct.pack('3i3f', param[0], param[1], param[2], param[3], param[4], param[5])

  
PackageDict = {MsgID.ID_SET_MOTOR:PackageSetMotor(),
               MsgID.ID_GET_MOTOR:PackageGetMotor()}

if __name__ == "__main__":
    import utime

    while True:
        pk_ID_GET_MOTOR = PackageDict[MsgID.ID_GET_MOTOR].pack()
        print(pk_ID_GET_MOTOR)
        print(struct.unpack('3i3f', pk_ID_GET_MOTOR))
        utime.sleep(1)
    
    # pk = PackageSetMotor()
    # data = pk.pack(0, 512, 0, 512, 0, 512)
    # print(data)
    # print(pk.unpack(data))
    # print(pk.dir1, pk.speed1, pk.dir2, pk.speed2, pk.dir3, pk.speed3)