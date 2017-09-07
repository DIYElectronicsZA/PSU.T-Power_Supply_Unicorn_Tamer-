import serial
import wx
import wx.grid as grid
import time
import io
import time
import logging
import sys
import glob
from serialfunctions import SerialPort

#3 parts
#1: User Display and interactions
#2: Serial connection
#3: Logic using User inputs

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
        """Class Constructor"""
        wx.Frame.__init__(self, parent, title=title)
        self.Show(True)

        # instantiate serial port class
        # #self.Panel_1 = UserDisplayPanel(myserialInstance)
        #self.Panel_1 = UserDisplayPanel(self)
        #self.Panel_1.set_Serial_Instance(self, myserialInstance)

        # Redundant 
        # Init Serial Handler class 
        #serial_handler = SerialHandler(self)

        # Init UserDisplayPanel class
        self.Panel_1 = UserDisplayPanel(self)

        # Send the comports list to the user display object Redundant? 
        #self.Panel_1.choices = comports_Class.Comports 
        
        #Using BoxSizer in wxPython to layout UserDisplayPanel
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.Panel_1, 0, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(sizer)
        self.SetBackgroundColour('#E2E3F3')
        self.Fit ()
        self.Centre()


#Visual display for users made up of two panels
class UserDisplayPanel(wx.Panel):
    
    # Class Variables
    serial_port = SerialPort()

    # choices = [] redundant? 
    port_to_connect = ""

    def __init__(self, parent):
        """Class Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent
        
        #Different font styles used throughout the display
        font = wx.Font(34, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        font2 = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        font3 = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        font4 = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        font5 = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
            
        #Settings label
        Settings_label = wx.StaticText(self, wx.ID_ANY, "Settings")
        Settings_label.SetFont(font)
        Settings_label.SetForegroundColour(wx.Colour(51,63,221))

        #Time label and textcntrl input for how long program should run
        Time_label = wx.StaticText(self, wx.ID_ANY, "Time")
        Time_label.SetFont(font2)
        self.Time_input = wx.TextCtrl(self, wx.ID_ANY, "10")

        #Min and Max Voltage label and text control input for parameters in logic
        Min_volt_label = wx.StaticText(self, wx.ID_ANY, "Minimum Voltage  ")
        Min_volt_label.SetFont(font2)
        self.Min_volt_input = wx.TextCtrl(self, wx.ID_ANY, "1")
        Max_volt_label = wx.StaticText(self, wx.ID_ANY, "Maximum Voltage  ")
        Max_volt_label.SetFont(font2)
        self.Max_volt_input = wx.TextCtrl(self, wx.ID_ANY, "2")

        #Min and Max Current label and text control input for parameters in logic
        Min_Amp_label = wx.StaticText(self, wx.ID_ANY, "Minimum Current   ")
        Min_Amp_label.SetFont(font2)
        self.Min_Amp_input = wx.TextCtrl(self, wx.ID_ANY, "3")
        Max_Amp_label = wx.StaticText(self, wx.ID_ANY, "Maximum Current   ")
        Max_Amp_label.SetFont(font2)
        self.Max_Amp_input = wx.TextCtrl(self, wx.ID_ANY, "4")

        ##Min and Max Temperature label and text control input for parameters in logic
        Min_temp_label = wx.StaticText(self, wx.ID_ANY, "Minimum Temp(C)")
        Min_temp_label.SetFont(font2)
        self.Min_temp_input = wx.TextCtrl(self, wx.ID_ANY, "5")
        Max_temp_label = wx.StaticText(self, wx.ID_ANY, "Maximum Temp(C)")
        Max_temp_label.SetFont(font2)
        self.Max_temp_input = wx.TextCtrl(self, wx.ID_ANY, "6")

        #Start/Stop button to start or end the program
        Start_Stop_button = wx.Button(self, label = "Submit")
        #Start_Stop_button.Bind(wx.EVT_BUTTON, self.Saving_inputs)
        Start_Stop_button.SetForegroundColour(wx.Colour(245,245,245))
        Start_Stop_button.SetFont(font3)
        Start_Stop_button.SetBackgroundColour('#000000')

        #Labels, combobox and button for selecting port
        Ports = wx.StaticText(self, wx.ID_ANY, "Available Ports") #Label for available ports
        Ports.SetFont(font2)
        self.Port_dropdown = wx.ComboBox(self, wx.ID_ANY) #ComboBox
        port_refresh = wx.Button(self, wx.ID_ANY, label= "refresh ports") #Refresh port button
        port_refresh.Bind(wx.EVT_BUTTON, self.refresh_dropdown(self))
        Select_port = wx.Button(self, wx.ID_ANY, label = 'Select port') #Select port button
        Select_port.Bind(wx.EVT_BUTTON, self.select_port)
        #Select_port.Bind(wx.EVT_BUTTON, self.on_timer)

        #Labels and values to update via logic for the current volt, current and temperature
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
        Overal_sizer = wx.BoxSizer(wx.VERTICAL) #Largest sizer
        Top_panel_sizer = wx.BoxSizer(wx.VERTICAL) #Sizer for top half of overall sizer
        Bottom_panel_sizer = wx.BoxSizer(wx.VERTICAL) #Sizer for Bottom half of overall sizer
        
        #Setting sizer
        Setting_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Setting_sizer.Add(Settings_label,0, wx.ALL, 5)
        
        #Time input sizer
        time_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        time_input_sizer.Add(Time_label, 0, wx.ALL,5)
        time_input_sizer.Add(self.Time_input,0, wx.ALL, 5)

        #Voltage input sizer
        Volt_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Volt_input_sizer.Add(Min_volt_label,0, wx.ALL, 5)
        Volt_input_sizer.Add(self.Min_volt_input,0, wx.ALL, 5)
        Volt_input_sizer.Add(Max_volt_label,0, wx.ALL, 5)
        Volt_input_sizer.Add(self.Max_volt_input,0, wx.ALL, 5)
        
        #Current input sizer
        Amp_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Amp_input_sizer.Add(Min_Amp_label, 0, wx.ALL, 5)
        Amp_input_sizer.Add(self.Min_Amp_input, 0, wx.ALL, 5)
        Amp_input_sizer.Add(Max_Amp_label, 0, wx.ALL, 5)
        Amp_input_sizer.Add(self.Max_Amp_input, 0, wx.ALL, 5)
        
        #Temperature input sizer
        Temp_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Temp_input_sizer.Add(Min_temp_label, 0, wx.ALL, 5)
        Temp_input_sizer.Add(self.Min_temp_input, 0, wx.ALL, 5)
        Temp_input_sizer.Add(Max_temp_label, 0, wx.ALL, 5)
        Temp_input_sizer.Add(self.Max_temp_input, 0, wx.ALL, 5)
        
        #Start/stop sizer
        Start_stop_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Start_stop_sizer.Add(Start_Stop_button, 0, wx.ALL,5)
        
        #Adding Setting, time, voltage, current, temperature inputs into TOP panel
        Top_panel_sizer.Add(Setting_sizer, 0, wx.ALL|wx.CENTER, 5)
        Top_panel_sizer.Add(time_input_sizer, 0, wx.ALL|wx.EXPAND, 5)
        Top_panel_sizer.Add(Volt_input_sizer, 0, wx.ALL|wx.EXPAND, 5)
        Top_panel_sizer.Add(Amp_input_sizer, 0, wx.ALL|wx.EXPAND, 5)
        Top_panel_sizer.Add(Temp_input_sizer, 0, wx.ALL|wx.EXPAND, 5)
        Top_panel_sizer.Add(Start_stop_sizer, 0, wx.ALL|wx.CENTER, 5)

        #Ports sizer
        ports_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ports_sizer.Add(Ports, 0, wx.ALL, 5)
        ports_sizer.Add(self.Port_dropdown, 0, wx.ALL, 5)
        ports_sizer.Add(Select_port, 0 , wx.ALL, 5)
        ports_sizer.Add(port_refresh, 0, wx.ALL, 5) 

        #Volt display sizer
        Volts_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Volts_sizer.Add(volts_value, 0, wx.ALL, 5)   
        Volts_sizer.Add(self.volts_value_update,0,wx.ALL, 5)

        #Amp display sizer
        Amp_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Amp_sizer.Add(Amps_value, 0, wx.ALL, 5)
        Amp_sizer.Add(self.Amps_value_update,0,wx.ALL, 5)

        #Temp display sizer
        Temp_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Temp_sizer.Add(Temp_value, 0, wx.ALL, 5)
        Temp_sizer.Add(self.Temp_value_update, 0,wx.ALL, 5)

        #Adding Ports components, Volt display, Amp display and Temp display to BOTTOM Panel
        Bottom_panel_sizer.Add(ports_sizer, 0, wx.ALL|wx.EXPAND,5)
        Bottom_panel_sizer.Add(Volts_sizer, 0, wx.ALL|wx.EXPAND , 5)
        Bottom_panel_sizer.Add(Amp_sizer, 0, wx.ALL| wx.EXPAND , 5)
        Bottom_panel_sizer.Add(Temp_sizer, 0, wx.ALL| wx.EXPAND , 5)

        #Adding Top and Bottom sizers to the overall sizer
        Overal_sizer.Add(Top_panel_sizer,0, wx.ALL|wx.LEFT, 5)
        Overal_sizer.Add(Bottom_panel_sizer, 0, wx.ALL|wx.CENTER, 5)

        #setup serial ports list: 
        #Its running anyway? TODO figure out why? 
        self.refresh_dropdown(self)
        
        self.SetSizer(Overal_sizer)
        Overal_sizer.Fit(self)
        self.Centre()

    def refresh_dropdown(self,event):
        ''' Method to refresh the list showing in the combobox found in the Bottom Panel in UserDisplayPanel ''' 

        print "Hi!"
        
        # Clear the comports list: 
        self.Port_dropdown.Clear()
        # Add the new comports
        self.Port_dropdown.Append(UserDisplayPanel.serial_port.serial_ports_list())

    def select_port(self,event):
        """Method to connect to a User selected port, ifelse statement to ensure a port is selected"""
        
        
        UserDisplayPanel.port_to_connect = self.Port_dropdown.GetValue() #Get Value from the ComboBox
        if len(UserDisplayPanel.port_to_connect) < 1:
            print "no port selected"
        else:
            UserDisplayPanel.serial_port.port_to_open = UserDisplayPanel.port_to_connect #Run Opening Port from Serialfunctions.py document
            UserDisplayPanel.serial_port.serial_port_open()     
            print "its open!"
        #self.serialvalues.serial_data()



# Redundant: 
#class SerialHandler(object):
    #''' Clever descrpiton for class :P ''' 

    # Class Variables: 

    #def __init__(self,event):
        #''' Class Constructor ''' 


    # Function to get a list of comports    
    #def get_Ports():
    #    self.serialvalues = serial_port()
    #    self.serialvalues.serial_ports_list()
    #    Comports = self.serialvalues.Comlist
        #UserDisplayPanel.choices = self.serialvalues.Comlist

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