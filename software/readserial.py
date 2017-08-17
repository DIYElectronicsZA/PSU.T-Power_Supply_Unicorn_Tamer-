import serial
import io

ser= serial.Serial('COM7', 115200)
while True:
	values_of_PSU = ser.readline()
	nwstuff = values_of_PSU.split(',')
	for stuff in nwstuff:
		print stuff[0:5]