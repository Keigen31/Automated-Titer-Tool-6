#include "controller.hpp"

int main(int argc, char *argv[])
{
    Controller controller = Controller();
    controller.connect_to_port("COM4");
    return 0;
}