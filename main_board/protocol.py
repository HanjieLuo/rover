import struct
from package import MsgID, PackageDict

# modified frame : header(2 bytes) + msg_len(2 bytes) + msg_len_chk(1 byte) + topic_id(2 bytes) + msg(x bytes) + msg_topic_id_chk(1 byte)

#   1st Byte - Sync Flag (Value: 0xff)
#   2th Byte - Message ID
#   3rd Byte - Message Length (N) - Low Byte
#   4th Byte - Message Length (N) - High Byte
#   x Bytes  - Serialized Message Data
#   Byte x+1 - Checksum over Message ID Message Length and Message Data

# Checksum over message length:
# msg_len_checksum = 255 - ( ((length&255) + (length>>8))%256 )
 
# Checksum over Topic ID and Message Data:
# msg_checksum = 255 - ( sum([ord(x) for x in msg]))%256 )

SYNC_FLAG = 0xff

class Status:
    WAITING_SYNC_FLAG = 0
    RECEIVE_MSG_ID = 1
    RECEIVE_MSG_LEN_LOW = 2
    RECEIVE_MSG_LEN_HIGH = 3
    RECEIVE_PACKAGE = 4
    RECEIVE_CHECKSUM = 5

class Protocol:
    def __init__(self, output_fun=None):
        self.status = Status.WAITING_SYNC_FLAG
        self.msg_id = 0
        self.msg_len = 0
        self.msg = bytearray()
        
        if output_fun is not None:
            self.print = output_fun.output
        else:
            self.print = print
    
    def parse(self, conn, buf):
        buf_len = len(buf)
        if buf_len == 0:
            return
        
        for i in range(buf_len):
            val = buf[i:i+1]
            if self.status is Status.WAITING_SYNC_FLAG:
                if ord(val) is SYNC_FLAG:
                    # print("WAITING_SYNC_FLAG")
                    self.msg_id = 0
                    self.msg_len = 0
                    self.data = bytearray()
                    self.package = bytearray()
                    self.status = Status.RECEIVE_MSG_ID
            
            elif self.status is Status.RECEIVE_MSG_ID:
                # print("RECEIVE_MSG_ID")
                self.data.extend(val)
                self.msg_id = ord(val)
                self.status = Status.RECEIVE_MSG_LEN_LOW
            
            elif self.status is Status.RECEIVE_MSG_LEN_LOW:
                # print("RECEIVE_MSG_LEN_LOW")
                self.data.extend(val)
                self.status = Status.RECEIVE_MSG_LEN_HIGH
                
            elif self.status is Status.RECEIVE_MSG_LEN_HIGH:
                # print("RECEIVE_MSG_LEN_HIGH")
                self.data.extend(val)
                self.msg_len, = struct.unpack("<H", self.data[-2:])
                if self.msg_len is 0:
                    self.status = Status.RECEIVE_CHECKSUM
                else:
                    self.status = Status.RECEIVE_PACKAGE
                # self.msg_len, = struct.unpack("<H", b''.join(self.msg[-2:]))
                # print(b''.join(self.msg[-2:]))
                
            elif self.status is Status.RECEIVE_PACKAGE:
                # print("RECEIVE_PACKAGE")
                self.package.extend(val)
                if len(self.package) == self.msg_len:
                    self.data.extend(self.package)
                    self.status = Status.RECEIVE_CHECKSUM
            
            elif self.status is Status.RECEIVE_CHECKSUM:
                # print("RECEIVE_CHECKSUM")
                self.status = Status.WAITING_SYNC_FLAG
                # print("checksum:", self.checksum(self.data))
                if ord(val) == self.checksum(self.data):
                    # print("Got a complete message.")
                    self.package_analysis(conn)
            
            else:
                self.status = Status.WAITING_SYNC_FLAG
    
    def checksum(self, data):
        return 255 - sum(data) % 256
    
    def package_analysis(self, conn):
        self.print("Get Msg ID:" + str(self.msg_id))
        pk = PackageDict[self.msg_id]
        if pk.unpack(self.package):
            if pk.need_response is True:
                data = self.make_command(self.msg_id)
                conn.send(data)
                self.print("Send Msg ID:" + str(self.msg_id))

    def make_command(self, msg_id, param=None):
        pkg = PackageDict[msg_id].pack(param)
        data = struct.pack("<BH", msg_id, len(pkg)) + pkg
        return struct.pack("B", SYNC_FLAG) + data + struct.pack("B", self.checksum(data))
        
                           
if __name__ == "__main__":
    protocol = Protocol()
    data = protocol.make_command(1, [2, 100, 2, 100, 2, 100])
    print(data)
    protocol.parse(None, data)



# modified frame : header(2 bytes) + msg_len(2 bytes) + msg_len_chk(1 byte) + topic_id(2 bytes) + msg(x bytes) + msg_topic_id_chk(1 byte)

#   1st Byte - Sync Flag (Value: 0xff)
#   2nd Byte - Sync Flag / Protocol version. The Protocol version byte was 0xff on ROS Groovy, 0xfe on ROS Hydro, Indigo, and Jade.
#   3rd Byte - Message Length (N) - Low Byte
#   4th Byte - Message Length (N) - High Byte
#   5th Byte - Checksum over message length
#   6th Byte - Topic ID - Low Byte. Topics ID 0-100 are reserved for system functions, 
#   7th Byte - Topic ID - High Byte
#   x Bytes  - Serialized Message Data
#   Byte x+1 - Checksum over Topic ID and Message Data

# special Topic ID
# uint16 ID_PUBLISHER=0
# uint16 ID_SUBSCRIBER=1
# uint16 ID_SERVICE_SERVER=2
# uint16 ID_SERVICE_CLIENT=4
# uint16 ID_PARAMETER_REQUEST=6
# uint16 ID_LOG=7
# uint16 ID_TIME=10
# uint16 ID_TX_STOP=11

# Checksum over message length:
# msg_len_checksum = 255 - ( ((length&255) + (length>>8))%256 )
 
# Checksum over Topic ID and Message Data:
# msg_checksum = 255 - ( ((topic&255) + (topic>>8) + sum([ord(x) for x in msg]))%256 )