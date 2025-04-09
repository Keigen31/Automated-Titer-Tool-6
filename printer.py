import serial
import time
#import threading

COMMANDBUFFERSIZE = 300
hSerial = None

XMOVEMENT = 0
YMOVEMENT = 0
ZMOVEMENT = 0
EMOVEMENT = 0

#SERIAL PORT CONNECTION SETUP
def connect_to_port(serial_port):
    global hSerial
    try:
        hSerial = serial.Serial(serial_port, baudrate=115200, timeout=0.05)
        print("Successfully Connected to Serial Port:", serial_port)
        
        # Clear input buffer
        #hSerial.reset_input_buffer()
        
        return hSerial
    
    except serial.SerialException:
        print("Serial port not found.")

def send_and_receive(hSerial, command):
    hSerial.write((command + "\n").encode())
    response = b""
    while True:
        response += hSerial.read(COMMANDBUFFERSIZE)
        if "ok\n" in response.decode():
            break
            
    print(response.decode())

        
def testing():           
    szBuff = "G0 Z20"
    send_and_receive(szBuff)
        
    time.sleep(10)
                    
    szBuff = "G0 Z90"
    send_and_receive(szBuff)
    time.sleep(5)
 
#SYRINGE FUNCTIONS 
      
def calculation(User_ratio):
    A = 1
    
    # Total Amount
    TotalAmount = 200  # microliter
    
    # Covert to actual volume
    C = TotalAmount / User_ratio # C is Sample volume A
    print("Bacteria volume in microL: ", C)
    
    D = TotalAmount - C # D is diluent volume 
    print("Buffer movement in microL: ", D)
    
    # Convert to distance
    x = ((C * 62) / 1000) # x is movement per C microliter
    print("Bacteria movement in mm: ", x)
    
    y = ((D * 62) / 1000)  # y is movement per D microliter
    print("Buffer movement in mm: ", y)
    return x, y
                          
        
def retract(amount):
    # Retract C amount
    send_and_receive(hSerial, "G1 E%.2f" % amount)
    print("Retracting: ", amount)
    
def extrude(amount):
    # Extrude C amount
    send_and_receive(hSerial, "G1 E-%.2f" % (amount + 5)) #going further than the home location to let all liquid escape
    send_and_receive(hSerial, "G4 P3000") #wait for 3 seconds to let all the liquid extruded
    print("Extruding: ", amount)       
        
#MAINLY THE FUNCTIONS TO CONTROL PRINTER MOVEMENT 
def fecth_buffer(bufferAmount):
    global XMOVEMENT
    global YMOVEMENT
    global ZMOVEMENT
    
    szBuff = "G0 X20 Y133 Z98 F9000" #Change X and Y to buffer flask location             
    send_and_receive(hSerial, szBuff)  
    XMOVEMENT += 40
    YMOVEMENT += 145
    ZMOVEMENT += 90
    
    szBuff = "G0 Z40"
    send_and_receive(hSerial, szBuff)
    ZMOVEMENT += 20
    
    #send_and_receive(hSerial, "G1 E-5")
    retract(bufferAmount)
                    
    szBuff = "G0 Z90"
    send_and_receive(hSerial,szBuff)
    
    retract(bufferAmount + 3 ) #extract a bit of airin to prevent liquid leaking
    ZMOVEMENT+ 90
          
    time.sleep(5)
    
            
def mixing(repeat_times = 3, up_duration = 1, down_duration = 1):    
    global ZMOVEMENT  
    for _ in range (repeat_times):
            
        szBuffUp = "G1 Z33"
        send_and_receive(hSerial,szBuffUp)
        time.sleep(up_duration)
        
        ZMOVEMENT+= 30
            
        szBuffDown = "G1 Z43"
        send_and_receive(hSerial,szBuffDown)
        time.sleep(down_duration)
        
        ZMOVEMENT+=35
        
def mixing_liquid(repeat_times = 3, up_duration = 1, down_duration = 1):    
    global ZMOVEMENT  
    for _ in range (repeat_times):
            
        szBuffUp = "G1 E10"
        send_and_receive(hSerial,szBuffUp)
        time.sleep(up_duration)
        
        ZMOVEMENT+= 30
            
        szBuffDown = "G1 E-10"
        send_and_receive(hSerial,szBuffDown)
        time.sleep(down_duration)
        
        ZMOVEMENT+=35
        
        
             
def buffer_move(userFactor, userNoSample, bufferAmount):
    global XMOVEMENT
    global YMOVEMENT
    global ZMOVEMENT
         
    baseString = "G0 X%d Y%d F9000"
       
    for x in range(22, 22 + ((userNoSample) * 9), +9):
        for y in range(33, 33 + ((userFactor) * 9), 9):    
            fecth_buffer(bufferAmount) #come and fetch buffer for every well
                
            szBuff = baseString % (x, y)
                
            send_and_receive(hSerial,szBuff)
            XMOVEMENT += x
            YMOVEMENT += y
        
            szBuff = "G1 Z38"
            send_and_receive(hSerial,szBuff)
            ZMOVEMENT += 30
            
            extrude(bufferAmount)
            
            send_and_receive(hSerial, "G4 P2000") #pause for 2 seconds
                    
            szBuff = "G1 Z50"
            send_and_receive(hSerial,szBuff)
            ZMOVEMENT += 50
            
            send_and_receive(hSerial, "G0 E0")
                              
        time.sleep(5)

#TIP CHANGING FEATURE           
def remove_tip():
    global XMOVEMENT
    global YMOVEMENT
    global ZMOVEMENT
    
    szBuff = "G0 X62 Y190 Z50 F9000" #Change X and Y and Z accordinly so the print head can stop in front of the remover              
    send_and_receive(hSerial,szBuff)
    XMOVEMENT += 60 
    YMOVEMENT += 190
    ZMOVEMENT += 50

    szBuff = "G0 Z32" #lower down
    send_and_receive(hSerial,szBuff)
    ZMOVEMENT += 28

    szBuff = "G0 Y206 F5000" #go into the remover space
    send_and_receive(hSerial,szBuff)
    YMOVEMENT += 204

    szBuff = "G0 Z70" #move up 
    send_and_receive(hSerial,szBuff)
    ZMOVEMENT += 50

    time.sleep(5)

#First tip location X121 Y204
def replace_tip():
    global XMOVEMENT
    global YMOVEMENT
    global ZMOVEMENT
    
    szBuff = "G0 Z70" #move up 
    send_and_receive(hSerial,szBuff)
    ZMOVEMENT += 70

    remove_tip() #go to the tip remover first 
    # A file to save the tip location, updated every time the printer finishes a run
    with open("tip_location.txt") as file:

            tipLocation = file.readline().strip()
            tipLocation_parts = tipLocation.split()

    tipX = float(tipLocation_parts[0])
    tipY = float(tipLocation_parts[1])

    print("Next tip to pick up: ", tipLocation)

    szBuff = "G0 X{} Y{}".format(tipX, tipY)     
    send_and_receive(hSerial,szBuff)
    XMOVEMENT += tipX 
    YMOVEMENT += tipY
    
    szBuff = "G0 Z32" #move down to pick up tip
    send_and_receive(hSerial, szBuff)
    ZMOVEMENT += 21
    
    mixing() #secure the tip in place 

    szBuff = "G0 Z90" #move up 
    send_and_receive(hSerial,szBuff)
    ZMOVEMENT += 85

    if(tipX < 220):
      tipX = tipX + 11.5
    else:
     tipX = 121
     tipY = tipY - 11.5
     

    with open('tip_location.txt', 'w') as file:
        file.write(f"{tipX} {tipY}")
      
    file.close()                      
    time.sleep(5)
        
            
def serial_dilution(userFactor, userNoSample, bacAmount):
    global XMOVEMENT
    global YMOVEMENT
    global ZMOVEMENT
    
    baseString = "G1 X%d Y%d F9000"
    
               
    for x in range(21, 22 + ((userNoSample) * 9), + 9):
        for y in range(23, 24 + ((userFactor) * 9), 9):
                
            szBuff = baseString % (x + 0.5, y + 0.5)
                
            send_and_receive(hSerial,szBuff)
            XMOVEMENT += x
            YMOVEMENT += y
           
           #coming down to the previous location and pick up 10% sample
            szBuff = "G1 Z40"
            send_and_receive(hSerial,szBuff)
            ZMOVEMENT += 40
            
            retract(bacAmount)
            
            szBuff = "G1 Z50"
            send_and_receive(hSerial,szBuff)
            ZMOVEMENT += 50
            retract(bacAmount + 5)
            
            szBuff = baseString % (x, y + 9) #moving to the next location to dispense and mix
            send_and_receive(hSerial,szBuff)
            XMOVEMENT += (x + 9)
            YMOVEMENT += (y+ 9)
            
            szBuff = "G1 Z40"
            send_and_receive(hSerial,szBuff)
            ZMOVEMENT += 40
            
            extrude(bacAmount) #dispend liquid here 
            send_and_receive(hSerial, "G4 P2000") #pause for 2 seconds

            mixing_liquid()
                     
            szBuff = "G1 Z50"
            send_and_receive(hSerial,szBuff)
            send_and_receive(hSerial, "G0 E0")
            ZMOVEMENT += 50
            
            replace_tip() #execute the tip replacing feature 
                             
        time.sleep(5)
 
 
    
#####COMPLETE TEST RUN#### 
def test_run(userNoSample, userNoFactor, userNoRatio): 
    global XMOVEMENT
    global YMOVEMENT
    global ZMOVEMENT
    
    bacteriaAmount, bufferAmount = calculation(userNoRatio) 
    print("Bacteria and buffer amount: ", bacteriaAmount, bufferAmount)
    
    buffer_move(userNoFactor, userNoSample, bufferAmount)
    
    replace_tip()
    
    serial_dilution(userNoFactor, userNoSample, bacteriaAmount)
    
    time.sleep(5)
        
##### BONUS FEATURES ######

def time_estimate(XMOVEMENT, YMOVEMENT, ZMOVEMENT, EMOVEMENT):

    x_time = XMOVEMENT / 400
    y_time = YMOVEMENT / 400
    z_time = ZMOVEMENT / 10
    e_time = EMOVEMENT / 25
    
    time_estimate = max(x_time, y_time, z_time, e_time)
    
    return time_estimate