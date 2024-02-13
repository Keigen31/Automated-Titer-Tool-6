from controller import Controller
import threading


def main():
    controller = Controller()
    controller.connect_to_port("COM15") #\.\COM16 and .\COM16
    
    userFactor = int(input("User enter dilute factor: "))
    userNoSample = int(input( "User enter the number of samples: "))
    
    #controller.send_and_receive("G1 X20 Y200 Z90 F9000")
    controller.send_and_receive("G28")
    
    controller.buffer_move(userFactor, userNoSample)
    #controller.fecth_buffer()
     
    
            

if __name__ == "__main__":
    main()