#ifndef CONTROLLER_HPP
#define CONTROLLER_HPP

#include <iostream>
#include <windows.h>
#include <string.h>

#define COMMANDBUFFERSIZE 300

using std::cout;
using std::string;

class Controller
{
public:
    Controller();
    void connect_to_port(const string& serial_port);
    void send_and_receive(const char* command);
    char send_buffer[COMMANDBUFFERSIZE];
    char receive_buffer[COMMANDBUFFERSIZE];
    DWORD bytes_written = 0;
    DWORD bytes_read = 0;
    int count = 0;
private:
    HANDLE hSerial;

};

#endif