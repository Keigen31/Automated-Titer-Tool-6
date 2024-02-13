#include "controller.hpp"

Controller::Controller()
{
   cout << "Controller Created\n";
}

void Controller::connect_to_port(const string& serial_port)
{
   LPCSTR L_serial_port = serial_port.c_str();
   this->hSerial = CreateFileA(L_serial_port,
                               GENERIC_READ | GENERIC_WRITE,
                               0,
                               0,
                               OPEN_EXISTING,
                               FILE_ATTRIBUTE_NORMAL,
                               0);
   if (hSerial == INVALID_HANDLE_VALUE)
   {
      if (GetLastError() == ERROR_FILE_NOT_FOUND)
      {
         cout << "Serial port not found.\n";
      }
   }
   else
   {
      cout << "Successfully Connected to Serial Port: " << serial_port << std::endl;
   }
   DCB dcbSerialParams = {0};
   dcbSerialParams.DCBlength = sizeof(dcbSerialParams);
   if (!GetCommState(hSerial, &dcbSerialParams))
   {
      // error getting state
      cout << "Failed to get current COM state.\n";
   }
   dcbSerialParams.BaudRate = CBR_115200;
   dcbSerialParams.ByteSize = 8;
   dcbSerialParams.StopBits = ONESTOPBIT;
   dcbSerialParams.Parity = NOPARITY;
   if (!SetCommState(hSerial, &dcbSerialParams))
   {
      // error setting serial port state
      cout << "Failed to set current COM state.\n";
   }
   COMMTIMEOUTS timeouts = {0};
   timeouts.ReadIntervalTimeout = 50;
   timeouts.ReadTotalTimeoutConstant = 50;
   timeouts.ReadTotalTimeoutMultiplier = 10;

   timeouts.WriteTotalTimeoutConstant = 50;
   timeouts.WriteTotalTimeoutMultiplier = 10;
   if (!SetCommTimeouts(hSerial, &timeouts))
   {
      // error occureed. Inform user
   }
}


void Controller::send_and_receive(const char* command)
{
   snprintf(send_buffer, COMMANDBUFFERSIZE, "%s\n", command);
   if (!WriteFile(hSerial, send_buffer, strlen(send_buffer), &(this->bytes_written), NULL))
   {
      cout << "Failed to write to port.\n";
   }

   
   while (1) {
      if (!ReadFile(hSerial, receive_buffer, COMMANDBUFFERSIZE, &(this->bytes_read), NULL)) 
      {
         cout << "Failed to read from port.\n";
         break;
      }
      receive_buffer[bytes_read] = '\0';

      // Verify command went through successfully
      if (strstr(receive_buffer, "ok") != NULL) {
         break;
      }
   }
}

// git add .
// git commit -m "Setting up send and read commands"
// git push