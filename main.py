from controller import Controller


def main():
    controller = Controller()
    controller.connect_to_port("COM15") #\.\COM16 and .\COM16
    
    #controller.send_and_receive("G1 X66 Y72 F9000")
    controller.send_and_receive("G28")
    
    #User enter the dilution factor
    userFactor = int(input("User enter dilute factor: "))
    
    #User enter the number of samples
    userNoSample = int(input("User enter number of samples: "))
     
    controller.buffer_move(userFactor, userNoSample)
    
    #while True:
        
        #user_ISR = input("Enter extra command: ").strip().lower()
        #if user_ISR == "pause": 
            #controller.pauseCommand()
            
        #elif user_ISR == "abort":
            #controller.abortCommand()
            

if __name__ == "__main__":
    main()