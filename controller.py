import serial

COMMANDBUFFERSIZE = 300

class Controller:
    def __init__(self):
        print("Controller Created")

    def connect_to_port(self, serial_port):
        try:
            self.hSerial = serial.Serial(serial_port, baudrate=115200, timeout=0.05)
            print("Successfully Connected to Serial Port:", serial_port)
        except serial.SerialException:
            print("Serial port not found.")

    def send_and_receive(self, command):
        self.hSerial.write((command + "\n").encode())
        response = b""
        while True:
            response += self.hSerial.read(COMMANDBUFFERSIZE)
            if b"ok" in response.decode():
                break

        print(response.decode())

