import serial
from guizero import App, Text, PushButton
import time

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
            if "ok\n" in response.decode():
                break
            
            

        print(response.decode())
        
    def buffer_move(self, userFactor, userNoSample):
        baseString = "G1 X%d Y%d\n"

        #userChoice = int(input("User enter dilute factor: "))
        #userNoSample = int(input "User enter the number of samples: ")

        for y in range(73, 73 - ((userFactor - 1) * 10), - 10):
            for x in range(68, 68 + (10 * (userNoSample - 1)), 10):
                szBuff = baseString % (x, y)
        
                if self.hSerial.write(szBuff.encode()) == 0:
                    print("Failed to write to port.")
            
                szBuff = "G0 Z0\n"
                if self.hSerial.write(szBuff.encode()) == 0:
                    print("Failed to write to port.")
            
                szBuff = "G0 Z20\n"
                if self.hSerial.write(szBuff.encode()) == 0:
                    print("Failed to write to port.")
            
        time.sleep(5)
     
    def pauseCommand(self):
        self.hSerial.write("M0\n".encode())
        Controller.send_and_receive("M0")
        Controller.send_and_receive(("M0" + "\n").encode())
        print("Controller Pause")        
    
    
    def abortCommand(self):
        self.hSerial.write("G28\n".encode())
        Controller.send_and_receive(("G28" + "\n").encode())
        print("Controller Reset")
    
     
        
    #An simple GUI, need to connect to Raspberry Pi first     
    #def gui(self):
        #app = App(title="guizero")

        #intro = Text(app, text="Welcome to Automated Titer Tool Team 6")
        #ok = PushButton(app, text="Enter")

        #app.display()
