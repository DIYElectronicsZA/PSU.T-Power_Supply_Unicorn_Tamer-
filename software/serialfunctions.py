import sys
import serial
#functions for serial port access
class serial_port(object):

    Comlist = []

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
        print serial_port.Comlist
    #opening serial port from user input choice
    def serial_port_open(self, serial_ports_list):
        port_to_open = ""
        serial_port_open.ser = serial.Serial(port_to_open, 115200)
        serial_port_open.ser.open()

    #reading serial and parsing values
    def serial_data(self, serial_port_open):
        value_PSU = serial_port_open.ser.readline()
        try:
            nwstuff = value_PSU.split(',')
            nwstuff[3] = nwstuff[3].replace(';',"")
            self.volts_value_update.SetLabel(str(nwstuff[1]))
            self.Amps_value_update.SetLabel(str(nwstuff[2]))
            self.Temp_value_update.SetLabel(str(nwstuff[3]))
        except:
            #continue
            print("Unexpected error:")
            #raise
            logger.debug('Unexpected error: Likely string was malformed & could not be split')
        wx.CallLater(100, self.serial_data)
    
    #close serial
    def close_serial(self, serial_port_open):
        serial_port_open.ser.close()

