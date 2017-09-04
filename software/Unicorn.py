import serial
import wx
import wx.grid as grid
import time
import io
import time
import logging
import sys
import glob

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

#Initiation class
class MainApp(wx.Frame):
    
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        self.Show(True)

        # instantiate serial port class
        # #self.Panel_1 = User_display(myserialInstance)
        #self.Panel_1 = User_display(self)
        #self.Panel_1.set_Serial_Instance(self, myserialInstance)
 
        classSerial = serial_port()
        classSerial.serial_ports_list()
        Values_for_drop_down = classSerial.Comlist
        self.Panel_1 = User_display(self)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.Panel_1, 0, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(sizer)
        self.SetBackgroundColour('#E2E3F3')
        self.Fit ()
        self.Centre()

#functions for serial port access
class serial_port():

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


#Visual display for users made up of two panels
class User_display(wx.Panel):
    # Class Constructor
    # Class Variables
    theSerial = serial_port
 
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent

        font = wx.Font(34, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        font2 = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        font3 = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        font4 = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        font5 = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        
        #Buttons and labels and text inputs for top panel.
        Settings_label = wx.StaticText(self, wx.ID_ANY, "Settings")
        Settings_label.SetFont(font)
        Settings_label.SetForegroundColour(wx.Colour(51,63,221))

        Time_label = wx.StaticText(self, wx.ID_ANY, "Time")
        Time_label.SetFont(font2)
        self.Time_input = wx.TextCtrl(self, wx.ID_ANY, "10")

        Min_volt_label = wx.StaticText(self, wx.ID_ANY, "Minimum Voltage  ")
        Min_volt_label.SetFont(font2)
        self.Min_volt_input = wx.TextCtrl(self, wx.ID_ANY, "1")

        Max_volt_label = wx.StaticText(self, wx.ID_ANY, "Maximum Voltage  ")
        Max_volt_label.SetFont(font2)
        self.Max_volt_input = wx.TextCtrl(self, wx.ID_ANY, "2")

        Min_Amp_label = wx.StaticText(self, wx.ID_ANY, "Minimum Current   ")
        Min_Amp_label.SetFont(font2)
        self.Min_Amp_input = wx.TextCtrl(self, wx.ID_ANY, "3")

        Max_Amp_label = wx.StaticText(self, wx.ID_ANY, "Maximum Current   ")
        Max_Amp_label.SetFont(font2)
        self.Max_Amp_input = wx.TextCtrl(self, wx.ID_ANY, "4")

        Min_temp_label = wx.StaticText(self, wx.ID_ANY, "Minimum Temp(C)")
        Min_temp_label.SetFont(font2)
        self.Min_temp_input = wx.TextCtrl(self, wx.ID_ANY, "5")

        Max_temp_label = wx.StaticText(self, wx.ID_ANY, "Maximum Temp(C)")
        Max_temp_label.SetFont(font2)
        self.Max_temp_input = wx.TextCtrl(self, wx.ID_ANY, "6")

        Start_Stop_button = wx.Button(self, label = "Submit")
        #Start_Stop_button.Bind(wx.EVT_BUTTON, self.Saving_inputs)
        Start_Stop_button.SetForegroundColour(wx.Colour(245,245,245))
        Start_Stop_button.SetFont(font3)
        Start_Stop_button.SetBackgroundColour('#000000')

        #Buttons, labels, txt cntrls and widgets for bottom panel
        Ports = wx.StaticText(self, wx.ID_ANY, "Available Ports")
        Ports.SetFont(font2)
        self.Port_dropdown = wx.ComboBox(self, wx.ID_ANY)
        port_refresh = wx.Button(self, wx.ID_ANY, label= "reset ports")
        #port_refresh.Bind(wx.EVT_BUTTON, self.Refreshbutton)

        #port_refresh.Bind(wx.EVT_BUTTON, self.serial_ports(self))
        #port_refresh.Bind(wx.EVT_BUTTON, Port_dropdown.Append(Logic_and_values.Comlist))

        Select_port = wx.Button(self, wx.ID_ANY, label = 'Select port')
        #Select_port.Bind(wx.EVT_BUTTON, self.select_port_button)
        #Select_port.Bind(wx.EVT_BUTTON, self.on_timer)
        volts_value = wx.StaticText(self, wx.ID_ANY, "Current Volts:")
        volts_value.SetFont(font2)
        self.volts_value_update = wx.StaticText(self, wx.ID_ANY, "Serial Volts")
        self.volts_value_update.SetFont(font3)
        self.volts_value_update.SetForegroundColour(wx.Colour(153,17,37))
        Amps_value = wx.StaticText(self, wx.ID_ANY, "Current Amps:")
        Amps_value.SetFont(font2)
        self.Amps_value_update = wx.StaticText(self, wx.ID_ANY, "Serial Amps")
        self.Amps_value_update.SetFont(font3)
        self.Amps_value_update.SetForegroundColour(wx.Colour(153,17,37))
        Temp_value = wx.StaticText(self, wx.ID_ANY, "Current Temp:")
        Temp_value.SetFont(font2)
        self.Temp_value_update = wx.StaticText(self, wx.ID_ANY, "Serial Temp")
        self.Temp_value_update.SetFont(font3)
        self.Temp_value_update.SetForegroundColour(wx.Colour(153,17,37))

        #Sizers used to insert widgets
        Overal_sizer = wx.BoxSizer(wx.VERTICAL)
        Top_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        Bottom_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        
        Setting_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Setting_sizer.Add(Settings_label,0, wx.ALL, 5)
        
        time_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        time_input_sizer.Add(Time_label, 0, wx.ALL,5)
        time_input_sizer.Add(self.Time_input,0, wx.ALL, 5)

    
        Volt_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Volt_input_sizer.Add(Min_volt_label,0, wx.ALL, 5)
        Volt_input_sizer.Add(self.Min_volt_input,0, wx.ALL, 5)
        Volt_input_sizer.Add(Max_volt_label,0, wx.ALL, 5)
        Volt_input_sizer.Add(self.Max_volt_input,0, wx.ALL, 5)
        
        Amp_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Amp_input_sizer.Add(Min_Amp_label, 0, wx.ALL, 5)
        Amp_input_sizer.Add(self.Min_Amp_input, 0, wx.ALL, 5)
        Amp_input_sizer.Add(Max_Amp_label, 0, wx.ALL, 5)
        Amp_input_sizer.Add(self.Max_Amp_input, 0, wx.ALL, 5)
        
        Temp_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Temp_input_sizer.Add(Min_temp_label, 0, wx.ALL, 5)
        Temp_input_sizer.Add(self.Min_temp_input, 0, wx.ALL, 5)
        Temp_input_sizer.Add(Max_temp_label, 0, wx.ALL, 5)
        Temp_input_sizer.Add(self.Max_temp_input, 0, wx.ALL, 5)
        
        Start_stop_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Start_stop_sizer.Add(Start_Stop_button, 0, wx.ALL,5)
        
        Top_panel_sizer.Add(Setting_sizer, 0, wx.ALL|wx.CENTER, 5)
        Top_panel_sizer.Add(time_input_sizer, 0, wx.ALL|wx.EXPAND, 5)
        Top_panel_sizer.Add(Volt_input_sizer, 0, wx.ALL|wx.EXPAND, 5)
        Top_panel_sizer.Add(Amp_input_sizer, 0, wx.ALL|wx.EXPAND, 5)
        Top_panel_sizer.Add(Temp_input_sizer, 0, wx.ALL|wx.EXPAND, 5)
        Top_panel_sizer.Add(Start_stop_sizer, 0, wx.ALL|wx.CENTER, 5)

        ports_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ports_sizer.Add(Ports, 0, wx.ALL, 5)
        ports_sizer.Add(self.Port_dropdown, 0, wx.ALL, 5)
        ports_sizer.Add(Select_port, 0 , wx.ALL, 5)
        ports_sizer.Add(port_refresh, 0, wx.ALL, 5) 

        Volts_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Volts_sizer.Add(volts_value, 0, wx.ALL, 5)   
        Volts_sizer.Add(self.volts_value_update,0,wx.ALL, 5)

        Amp_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Amp_sizer.Add(Amps_value, 0, wx.ALL, 5)
        Amp_sizer.Add(self.Amps_value_update,0,wx.ALL, 5)

        Temp_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Temp_sizer.Add(Temp_value, 0, wx.ALL, 5)
        Temp_sizer.Add(self.Temp_value_update, 0,wx.ALL, 5)

        Bottom_panel_sizer.Add(ports_sizer, 0, wx.ALL|wx.EXPAND,5)
        Bottom_panel_sizer.Add(Volts_sizer, 0, wx.ALL|wx.EXPAND , 5)
        Bottom_panel_sizer.Add(Amp_sizer, 0, wx.ALL| wx.EXPAND , 5)
        Bottom_panel_sizer.Add(Temp_sizer, 0, wx.ALL| wx.EXPAND , 5)

        Overal_sizer.Add(Top_panel_sizer,0, wx.ALL|wx.LEFT, 5)
        Overal_sizer.Add(Bottom_panel_sizer, 0, wx.ALL|wx.CENTER, 5)
        
        self.SetSizer(Overal_sizer)
        Overal_sizer.Fit(self)
        self.Centre()

    # Function to set instance of the serial port class. 
    #def set_Serial_Instance(self, serial_port passedSerial):
    #    theSerial = passedSerial

    # Function to do things, like read serial
    #def read_Serial():
        # error checking
        #if theSerial != null
            #theSerial.read()
 

app = wx.App(False)
MainApp(None, "PS Unicorn")
app.MainLoop()