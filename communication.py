import serial
import time

serialaddress = input('usbModem : ')
SerialObj = serial.Serial(serialaddress)                # COMxx  format on Windows
                                                        # ttyUSBx format on Linux
SerialObj.baudrate = 74880                              # set Baud rate to 9600
SerialObj.bytesize = 8                                  # Number of data bits = 8
SerialObj.parity  = 'N'                                  # No parity
SerialObj.stopbits = 1                                  # Number of Stop bits = 1
time.sleep(3)

# SerialObj.write(input('Message to send : '))    #transmit a message to micro/Arduino
# SerialObj.close()      # Close the port


def send_message(message):
    global SerialObj
    try:
        SerialObj.write(bytes(message, 'utf8'))
    except Exception as e:
        if str(e) == "write failed: [Errno 6] Device not configured":
            time.sleep(1)
            SerialObj = serial.Serial(serialaddress)
            send_message(message)
        else:
            print("Error in sending message : ", e)
        
    time.sleep(1)

if __name__ == "__main__":
    try :
        while True:
            send_message(input("Message to send : "))
    except KeyboardInterrupt:
        print("Exiting the program")
        SerialObj.close()      # Close the port
