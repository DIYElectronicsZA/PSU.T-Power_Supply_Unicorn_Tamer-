import serial
import numpy as np
import time
import sys
import matplotlib.pyplot as plt
 
ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM8'
ser.open()
one_list = []
stime = np.array([])
test_num = 0
for serial_output in ser:
 
    listing = []  
    plt.ion()
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
        newtime = time.clock()
        stime = np.append(stime, newtime)
        print one_list
        plt.plot(stime,one_list, 'ro')
        plt.pause(0.5)

    except:
 
        continue
 

 