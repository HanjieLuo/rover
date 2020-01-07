import pygatt

class BleClient:
    def __init__(self, address="", port="COM4"):
        adapter = pygatt.BGAPIBackend(serial_port=port)
        adapter.start()

        print("start")
        devices = adapter.scan(timeout=1)
        print(len(devices))
        for dev in devices:
            print("address: %s, name: %s " % (dev['address'], dev['name']))


if __name__ == '__main__':
    client = BleClient()