from controller import Controller

def main():
    controller = Controller()
    controller.connect_to_port("COM4")

if __name__ == "__main__":
    main()
