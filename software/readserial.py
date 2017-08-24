import serial
countdown = 300
ser= serial.Serial('COM7', 115200)
while countdown > 0:
    values_of_PSU = ser.readline()
    nwstuff = values_of_PSU.split(',')
    
    try:
        countdown = countdown - 1
        print nwstuff
        print nwstuff[0]
        print nwstuff[1]
        print nwstuff[2]
        nwstuff[3] = nwstuff[3].replace(';', "")
        print nwstuff[3]
        print '\n'
    except:
        continue