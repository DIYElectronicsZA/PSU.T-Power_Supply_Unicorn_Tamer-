import serial
import numpy as np

ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM8'
ser.open()

one_list = []
test_num = 0
for serial_output in ser:
    listing = []  
    try:
        serial_output = serial_output.split(',')
        serial_output[3] = serial_output[3].replace(';', "")
        serial_output[3] = serial_output[3].strip('\r\n')
        serial_output[1] = float(serial_output[1])
        serial_output[2] = float(serial_output[2])
        serial_output[3] = float(serial_output[3])
        test_num = test_num + 1
        listing.append(test_num)
        listing.append(serial_output[1])
        listing.append(serial_output[2])
        listing.append(serial_output[3])
        one_list.append(listing)
        print one_list
        for i in one_list:
            print i
    except:
        continue


