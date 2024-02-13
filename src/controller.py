import serial
#from guizero import App, Text, PushButton
import time
import threading

COMMANDBUFFERSIZE = 300

class Controller:
    def __init__(self):
        self.paused = threading.Event()
        self.abort_flag = False
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

    def fecth_buffer(self):
        baseString = "G1 X20 Y200 Z90 F9000" #Change X and Y to buffer flask location
        
        szBuff = baseString
                
        self.send_and_receive(szBuff)
        
        if self.hSerial.write(szBuff.encode()) != len(szBuff):
            print("Failed to write to port.")
            
        
        szBuff = "G1 Z30 F9000"
        self.send_and_receive(szBuff)
        if self.hSerial.write(szBuff.encode()) == 0:
            print("Failed to write to port.")
                    
        szBuff = "G1 Z90 F9000"
        self.send_and_receive(szBuff)
        if self.hSerial.write(szBuff.encode()) == 0:
            print("Failed to write to port.")
            
        time.sleep(5)
    
 
            
    def mixing(self):    
                         
        szBuff = "G1 Z20"
        self.send_and_receive(szBuff)
        if self.hSerial.write(szBuff.encode()) != len(szBuff):
            print("Failed to write to port.")
        szBuff = "G1 Z5"
        if self.hSerial.write(szBuff.encode()) != len(szBuff):
                print("Failed to write to port.")
        szBuff = "G1 Z20"
        self.send_and_receive(szBuff)
        if self.hSerial.write(szBuff.encode()) != len(szBuff):
            print("Failed to write to port.")
        szBuff = "G1 Z5"
        if self.hSerial.write(szBuff.encode()) != len(szBuff):
                print("Failed to write to port.")
            
        
             
    def buffer_move(self, userFactor, userNoSample):  
        self.fecth_buffer()
        
        baseString = "G1 X%d Y%d F9000"

        for y in range(73, 73 - ((userFactor) * 10), - 10):
            for x in range(68, 68 + (10 * (userNoSample)), 10):
                
                szBuff = baseString % (x, y)
                
                self.send_and_receive(szBuff)
        
                #if self.hSerial.write(szBuff.encode()) == 0:
                if self.hSerial.write(szBuff.encode()) != len(szBuff):
                    print("Failed to write to port.")
            
                szBuff = "G1 Z10 F9000"
                self.send_and_receive(szBuff)
                #if self.hSerial.write(szBuff.encode()) == 0:
                if self.hSerial.write(szBuff.encode()) != len(szBuff):
                    print("Failed to write to port.")
            
                szBuff = "G1 Z30 F9000"
                self.send_and_receive(szBuff)
                #if self.hSerial.write(szBuff.encode()) == 0:
                if self.hSerial.write(szBuff.encode()) != len(szBuff):
                    print("Failed to write to port.")
                    
            
                              
            time.sleep(1)
            
         
    def pause(self):
        self.pause.set()
        
    def resume(self):
        self.pause.clear()
        
    def abort(self):
        self.abort_flag = True
        self.pause.set()
    
    
        
