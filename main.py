import printer as Printer
import GUI as gui
import serial 
import tkinter as tk
import time   
import tkinter.font as tkFont
import math
import subprocess
import os      

EXTRUDER_HOME = 0
gui.START_FLAG


def main():
    print("The amount of sample user has input in: ", gui.SAMPLE_VALUE)
    print("The dilution factor user has input in: ", gui.DILU_FAC_VALUE)
    print("The dilution ratio user has input in: ", gui.DILU_RATI_VALUE)
    SAMPLE_VALUE = int(gui.SAMPLE_VALUE)
    DILU_FAC_VALUE = int(gui.DILU_FAC_VALUE)
    DILU_RATI_VALUE = int(gui.DILU_RATI_VALUE)
        
   
    if gui.START_FLAG == 1: 
        hSerial = Printer.connect_to_port("COM15") 
        print("Checkpoint 1")    
        #Printer.send_and_receive(hSerial, "M112")
        #hSerial.reset_input_buffer()   
        
        
        if hSerial: 
            print("Checkpoint 2")
            
            Printer.send_and_receive(hSerial, "M302 P1") #disable hot print
            
            print("Checkpoint hotprint")
        
            Printer.send_and_receive(hSerial, "M92 E81.5") #setting 81.5 steps/mm. 62mm/1ml
            
            Printer.send_and_receive(hSerial, "M220 S80") #set all axis speed to 20% lower
        
            Printer.send_and_receive(hSerial, "G90") #setting absolute coordination

            Printer.send_and_receive(hSerial, "G28") #homing XYZ
            
            Printer.send_and_receive(hSerial, "G92 E0") #set the current position at home position for extruder
            
            
            #Printer.send_and_receive(hSerial, "G1 Z40")
            
            #Printer.send_and_receive(hSerial, "G0 E0")
            
            #Printer.send_and_receive(hSerial, "G1 X20 Y133 Z98")
            
            #Printer.send_and_receive(hSerial, "G1 Z40")
                      
            #Printer.send_and_receive(hSerial, "G0 E12.4") #absolute coor
            
            #Printer.send_and_receive(hSerial, "G1 Z80")
            
            #Printer.send_and_receive(hSerial, "G4 P5000")
            
            #Printer.send_and_receive(hSerial, "M220 S80")
            
            #Printer.send_and_receive(hSerial, "G1 Z90")
            
            #Printer.send_and_receive(hSerial, "G0 E15.4") #withdraw air
            
           # Printer.send_and_receive(hSerial, "G4 P2000")
            
           ## Printer.send_and_receive(hSerial, "G0 E-10")
            
           # Printer.send_and_receive(hSerial, "G4 P2000")
            
           # Printer.send_and_receive(hSerial, "G0 E0")
            
            #Printer.send_and_receive(hSerial, "G1 X30 Y40")
            
            #Printer.send_and_receive(hSerial, "G1 Z40")
            
            #time.sleep(5)
            
            #Printer.send_and_receive(hSerial, "G1 E-19.3")
            
            
            
            print("Checkpoint 3")
            
            #Printer.send_and_receive(hSerial, "G0 Z40")
            
            
        #testing the function with user input paramters from GUI
            Printer.test_run(SAMPLE_VALUE, DILU_FAC_VALUE, DILU_RATI_VALUE)
                     
        #testing the estimated time clock 
            print("Time will take to run: ", Printer.time_estimate(Printer.XMOVEMENT, Printer.YMOVEMENT, Printer.ZMOVEMENT, Printer.EMOVEMENT))
            
        #end a run and rest the buffer 
            #hSerial.reset_input_buffer()   
            
            
            if hSerial: 
                print("Checkpoint 2")
                
                Printer.send_and_receive(hSerial, "M302 P1") #disable hot print
                
                print("Checkpoint hotprint")
            
                Printer.send_and_receive(hSerial, "M92 E81.5") #setting 81.5 steps/mm. 62mm/1ml
                
                Printer.send_and_receive(hSerial, "M220 S80") #set all axis speed to 20% lower
            
                Printer.send_and_receive(hSerial, "G90") #setting absolute coordination

                Printer.send_and_receive(hSerial, "G28") #homing XYZ
                
                Printer.send_and_receive(hSerial, "G92 E0") #set the current position at home position for extruder
                    
                
                print("Checkpoint 3")
                
                #Printer.send_and_receive(hSerial, "G0 Z40")
                
                
            #testing the function with user input paramters from GUI
                Printer.test_run(SAMPLE_VALUE, DILU_FAC_VALUE, DILU_RATI_VALUE)
                        
            #testing the estimated time clock 
                print("Time will take to run: ", Printer.time_estimate(Printer.XMOVEMENT, Printer.YMOVEMENT, Printer.ZMOVEMENT, Printer.EMOVEMENT))
                
            #end a run and rest the buffer 
                #hSerial.reset_input_buffer()   
        else:
            print("Haven't press START yet.")
        time.sleep(1)
               
   
if __name__ == "__main__":
    main()  
