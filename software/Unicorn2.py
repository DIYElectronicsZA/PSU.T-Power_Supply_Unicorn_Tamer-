import serial
import wx
import wx.grid as grid
import time
import io
import time
import logging

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

import sys
import glob




# Main Class 
class MainApp(wx.Frame):
    
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        self.Show(True)

        # Init Values Class
        self.Panel_1 = Values_of_PSU(self)
        # Init Logic Class
        self.Panel_2 = Logic_and_values(self)


        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.Panel_1, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(self.Panel_2, 0, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(sizer)
        self.SetBackgroundColour('#E2E3F3')
        self.Fit ()
        self.Centre()

# Values class? 
class Values_of_PSU(wx.Panel):
    # Init Class variables
    MinVolt = 0
    MaxVolt = 0
    MinAmp = 0
    MaxAmp = 0
    MinTemp = 0
    MaxTemp = 0
    
    # Class Constructor 
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent

        font = wx.Font(34, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        font2 = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        font3 = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        
        #Buttons, Text controls, widgets, values etc
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
        Start_Stop_button.Bind(wx.EVT_BUTTON, self.Saving_inputs)
        Start_Stop_button.SetForegroundColour(wx.Colour(245,245,245))
        
        Start_Stop_button.SetFont(font3)
        Start_Stop_button.SetBackgroundColour('#000000')

        Overal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Left_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        Right_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        
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
        
        Left_panel_sizer.Add(Setting_sizer, 0, wx.ALL|wx.CENTER, 5)
        Left_panel_sizer.Add(time_input_sizer, 0, wx.ALL|wx.EXPAND, 5)
        Left_panel_sizer.Add(Volt_input_sizer, 0, wx.ALL|wx.EXPAND, 5)
        Left_panel_sizer.Add(Amp_input_sizer, 0, wx.ALL|wx.EXPAND, 5)
        Left_panel_sizer.Add(Temp_input_sizer, 0, wx.ALL|wx.EXPAND, 5)
        Left_panel_sizer.Add(Start_stop_sizer, 0, wx.ALL|wx.CENTER, 5)

        Overal_sizer.Add(Left_panel_sizer,0, wx.ALL|wx.LEFT, 5)
        
        self.SetSizer(Overal_sizer)
        Overal_sizer.Fit(self)

    # Function which assigns text-box values to class globals
    def Saving_inputs(self, event):
        Values_of_PSU.TimeValue = self.Time_input.GetValue()
        Values_of_PSU.MaxVolt = self.Max_volt_input.GetValue()
        Values_of_PSU.MinVolt = self.Min_volt_input.GetValue()
        Values_of_PSU.MinAmp = self.Min_Amp_input.GetValue()
        Values_of_PSU.MaxAmp = self.Max_Amp_input.GetValue()
        Values_of_PSU.MinTemp = self.Min_temp_input.GetValue()
        Values_of_PSU.MaxTemp = self.Max_temp_input.GetValue()

# Logic class 
class Logic_and_values(wx.Panel):

    # Class Constructor
    Comlist = []
    
    def __init__(self, parent):
        self.serial_ports(self)
        print Logic_and_values.Comlist
        #Logic_and_values.ser = serial.Serial(
        #port='COM7',
        #baudrate=115200)
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent

        font2 = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        font3 = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.BOLD)

        Ports = wx.StaticText(self, wx.ID_ANY, "Available Ports")
        Ports.SetFont(font2)
        self.Port_dropdown = wx.ComboBox(self, wx.ID_ANY, choices = Logic_and_values.Comlist)
        port_refresh = wx.Button(self, wx.ID_ANY, label= "reset ports")
        port_refresh.Bind(wx.EVT_BUTTON, self.Refreshbutton)
        #port_refresh.Bind(wx.EVT_BUTTON, self.serial_ports(self))
        #port_refresh.Bind(wx.EVT_BUTTON, Port_dropdown.Append(Logic_and_values.Comlist))
        Select_port = wx.Button(self, wx.ID_ANY, label = 'Select port')
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

        Overal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Left_panel_sizer = wx.BoxSizer(wx.VERTICAL)

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

        Left_panel_sizer.Add(ports_sizer, 0, wx.ALL|wx.EXPAND,5)
        Left_panel_sizer.Add(Volts_sizer, 0, wx.ALL|wx.EXPAND , 5)
        Left_panel_sizer.Add(Amp_sizer, 0, wx.ALL| wx.EXPAND , 5)
        Left_panel_sizer.Add(Temp_sizer, 0, wx.ALL| wx.EXPAND , 5)

        Overal_sizer.Add(Left_panel_sizer, 0, wx.ALL|wx.CENTER, 5)
        self.SetSizer(Overal_sizer)
        Overal_sizer.Fit(self)
        self.Centre()

        # ser.open()

        #self.on_timer()
    def Refreshbutton(self,event):
        Logic_and_values.serial_ports(self,event)
        self.Port_dropdown.Clear()
        self.Port_dropdown.Append(Logic_and_values.Comlist)   
    def serial_ports(self, event):
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
        Logic_and_values.Comlist = result
        return result

    def on_timer(self):
        countdown = 30
        
        while countdown > 0:
            value_PSU = Logic_and_values.ser.readline()
            #print value_PSU
            try:
                countdown = countdown - 1
                nwstuff = value_PSU.split(',')
                nwstuff[3] = nwstuff[3].replace(';',"")
                MinMaxThresh(self)
            except:
                continue
        
        self.volts_value_update.SetLabel(str(nwstuff[1]))
        self.Amps_value_update.SetLabel(str(nwstuff[2]))
        self.Temp_value_update.SetLabel(str(nwstuff[3]))
        wx.CallLater(1000, self.on_timer)
        return nwstuff
        
        

        value_PSU = ser.readline()
        try:
            nwstuff = value_PSU.split(',')
            nwstuff[3] = nwstuff[3].replace(';',"")
            self.volts_value_update.SetLabel(str(nwstuff[1]))
            self.Amps_value_update.SetLabel(str(nwstuff[2]))
            self.Temp_value_update.SetLabel(str(nwstuff[3]))
        except:
            #continue
            #print("Unexpected error:")
            #raise
            logger.debug('Unexpected error: Likely string was malformed & could not be split')
        wx.CallLater(100, self.on_timer)

    
    
app = wx.App(False)
MainApp(None, "PS Unicorn")
app.MainLoop()
