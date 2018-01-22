import logging
import sys
import serial

#Setup Debug Logging
#From https://inventwithpython.com/blog/2012/04/06/stop-using
# -print-for-debugging-a-5-minute-quickstart-guide-to-pythons-logging-module/
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

class SerialPort(object):
    """Class containing functions to list available Comports,
    Open a serial port, close a serial port and read data from a serial port"""
    Comlist = []
    ser = ""
    port = ''
    volts = '0'
    amps = '0'
    temp = '0'
    port2 = ''
    volts2 = '0'
    amps2 = '0'
    temp2 = '0'
    error_on = 0
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
        SerialPort.Comlist = result
        return result
    #opening serial port from user input choice

    def serial_port_open(self, Port_To_Open):
        """Method to open serial port"""
        self.error_on = self.error_on + 5
        print self.error_on
        self.port_to_open = Port_To_Open
        SerialPort.ser = serial.Serial(self.port_to_open, 115200)
        SerialPort.ser.close()
        SerialPort.ser.open()
        

    #reading serial and parsing values
    def serial_data(self):        
        serial_list = []
        #serial_lines = SerialPort.ser.readline()
        for serial_output in SerialPort.ser:
            try:
                channels = int(serial_output[0])
            except:
                continue
                #if serial_ouput isnt int

            one_list = []
            if channels == 1:
                listing = []
                test_num = 0
                try:
                    #print serial_output
                    serial_output = serial_output.split(',')
                    serial_list.append(serial_output)
                    serial_output[3] = serial_output[3].replace(';', "")
                    serial_output[3] = serial_output[3].strip('\r\n')

                    SerialPort.port  = serial_output[0]
                    SerialPort.volts = serial_output[1]
                    SerialPort.amps  = serial_output[2]
                    SerialPort.temp  = serial_output[3]

                    serial_output[1] = float(serial_output[1])
                    serial_output[2] = float(serial_output[2])
                    serial_output[3] = float(serial_output[3])
                    test_num = test_num + 1
                    listing.append(test_num)
                    listing.append(serial_output[1])
                    listing.append(serial_output[2])
                    listing.append(serial_output[3])
                    one_list.append(listing)
                except:
                    continue

            two_list = 0
            if channels == 2:
                listing = []
                test_num = 0
                try:
                    #print serial_output
                    serial_output = serial_output.split(',')
                    serial_list.append(serial_output)
                    serial_output[3] = serial_output[3].replace(';', "")
                    serial_output[3] = serial_output[3].strip('\r\n')

                    SerialPort.port2  = serial_output[0]
                    SerialPort.volts2 = serial_output[1]  
                    SerialPort.amps2  = serial_output[2] 
                    SerialPort.temp2  = serial_output[3]

                    serial_output[1] = float(serial_output[1])
                    serial_output[2] = float(serial_output[2])
                    serial_output[3] = float(serial_output[3])

                    test_num = test_num + 1
                    listing.append(test_num)
                    listing.append(serial_output[1])
                    listing.append(serial_output[2])
                    listing.append(serial_output[3])
                    two_list.append(listing)
                except:
                    continue
            else:
                continue


    #close serial
    def close_serial(self):
        """Function to close serial port connection"""
        try:
            self.error_on = self.error_on - 5
            SerialPort.ser.close()
        except:
            print "Kill me BEN!"
