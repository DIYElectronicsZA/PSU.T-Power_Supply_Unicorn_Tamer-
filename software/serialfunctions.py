import sys
import serial
import logging
#functions for serial port access
#Setup Debug Logging 
#From https://inventwithpython.com/blog/2012/04/06/stop-using-print-for-debugging-a-5-minute-quickstart-guide-to-pythons-logging-module/
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# File Logging 
#enable this to log to file
#fh = logging.FileHandler('log_filename.txt')
#fh.setLevel(logging.DEBUG)
#fh.setFormatter(formatter)
#logger.addHandler(fh)

# Debug Console
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.debug('Welcome to Power Supply Unicorn Tamer :)')

class serial_port(object):

    Comlist = []
    ser = ""
    port_to_open = ""
    #Listing available ports for serial
    def serial_ports_list(self):
        """ Lists serial port names
    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of the serial ports available on the system
    """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
    # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        serial_port.Comlist = result
    #opening serial port from user input choice

    def serial_port_open(port_to_open):
        ser = serial.Serial(serial_port.port_to_open, 115200)
        ser.close()
        ser.open()

    #reading serial and parsing values
    def serial_data():
        value_PSU = ser.readline()
        for lines in value_PSU:
            print lines
    
    #close serial
    def close_serial(port_to_open):
        serial_port.ser.close()

print "Kill me BEN!"