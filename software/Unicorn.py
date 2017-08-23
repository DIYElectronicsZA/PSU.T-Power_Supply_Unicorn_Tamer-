import serial
import wx
import wx.grid as grid
import time
import io
import time

class MainApp(wx.Frame):
    
    def __init__(self, parent, title):
        wx.Frame.__init__(self,parent,title=title)
        self.Show(True)
        self.Panel = Values_of_PSU(self)
        self.SetBackgroundColour('#F8F2DA')
        self.Fit()

class Values_of_PSU(wx.Panel):
    MinVolt = 0
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent
        Values_of_PSU.MinVolt = 0
        

        self.timer =wx.Timer(self)
        #self.Bind(wx.EVT_TIMER, self.update, self.timer)
        font = wx.Font(32, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        font2 = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        font3 = wx.Font(16, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        #Buttons, Text controls, widgets, values etc
        
        Settings_label = wx.StaticText(self, wx.ID_ANY, "Settings")
        Settings_label.SetFont(font)
        Time_label = wx.StaticText(self, wx.ID_ANY, "Time")
        Time_label.SetFont(font2)
        self.Time_input = wx.TextCtrl(self, wx.ID_ANY, "10")
        
        #Countdown_value = 
        Min_volt_label = wx.StaticText(self, wx.ID_ANY, "Minimum Voltage threshold  ")
        Min_volt_label.SetFont(font2)
        self.Min_volt_input = wx.TextCtrl(self, wx.ID_ANY, "1")
        Max_volt_label = wx.StaticText(self, wx.ID_ANY, "Maximum Voltage threshold  ")
        Max_volt_label.SetFont(font2)
        self.Max_volt_input = wx.TextCtrl(self, wx.ID_ANY, "2")
        Min_Amp_label = wx.StaticText(self, wx.ID_ANY, "Minimum Current threshold   ")
        Min_Amp_label.SetFont(font2)
        self.Min_Amp_input = wx.TextCtrl(self, wx.ID_ANY, "3")
        Max_Amp_label = wx.StaticText(self, wx.ID_ANY, "Maximum Current threshold   ")
        Max_Amp_label.SetFont(font2)
        self.Max_Amp_input = wx.TextCtrl(self, wx.ID_ANY, "4")
        Min_temp_label = wx.StaticText(self, wx.ID_ANY, "Minimum Temp(C) threshold")
        Min_temp_label.SetFont(font2)
        self.Min_temp_input = wx.TextCtrl(self, wx.ID_ANY, "5")
        Max_temp_label = wx.StaticText(self, wx.ID_ANY, "Maximum Temp(C) threshold")
        Max_temp_label.SetFont(font2)
        self.Serialvalue = wx.StaticText(self,wx.ID_ANY, label = "Serial")
        self.Max_temp_input = wx.TextCtrl(self, wx.ID_ANY, "6")
        Start_Stop_button = wx.Button(self, label = "Start/Stop")
        Reset_button = wx.Button(self, label= "Reset values")
        Start_Stop_button.SetFont(font3)
        Start_Stop_button.SetBackgroundColour('#DDECEF')
        Start_Stop_button.Bind(wx.EVT_BUTTON, self.Saving_inputs)
        #Start_Stop_button.Bind(wx.EVT_BUTTON, self.SerialReader)
        Reset_button.SetFont(font3)
        Reset_button.SetBackgroundColour('#DDECEF')
        
        #Voltage_realtime_label = wx.StaticText(self, wx.ID_ANY, "Volts")
        #Amp_realtime_label = wx.StaticText(self, wx.ID_ANY, "Amps")
        #Temp_realtime_label = wx.StaticText(self, wx.ID_ANY, "Temp")
        
        
        #Volts_graph =
        #Amp_graph =
        #Temp_graph =
        
        #Layout
        
        Overal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Left_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        Right_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        
        Setting_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Setting_sizer.Add(Settings_label,0, wx.ALL, 5)
        
        time_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        time_input_sizer.Add(Time_label, 0, wx.ALL,5)
        time_input_sizer.Add(self.Time_input,0, wx.ALL, 5)
        time_input_sizer.Add(self.Serialvalue,0, wx.ALL, 5)
        
        
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
        Start_stop_sizer.Add(Reset_button, 0, wx.ALL, 5)
        
        Left_panel_sizer.Add(Setting_sizer, 0, wx.ALL|wx.CENTER, 5)
        Left_panel_sizer.Add(time_input_sizer, 0, wx.ALL|wx.EXPAND, 5)
        Left_panel_sizer.Add(Volt_input_sizer, 0, wx.ALL|wx.EXPAND, 5)
        Left_panel_sizer.Add(Amp_input_sizer, 0, wx.ALL|wx.EXPAND, 5)
        Left_panel_sizer.Add(Temp_input_sizer, 0, wx.ALL|wx.EXPAND, 5)
        Left_panel_sizer.Add(Start_stop_sizer, 0, wx.ALL|wx.CENTER, 5)
        
        #Volt_realtime_sizer = wx.BoxSizer(wx.HORIZONTAL)
        #Volt_realtime_sizer.Add(Voltage_realtime_label, 0, wx.ALL, 5)
        
        #Amp_realtime_sizer = wx.BoxSizer(wx.HORIZONTAL)
        #Amp_realtime_sizer.Add(Amp_realtime_label, 0, wx.ALL, 5)
        
        #Temp_realtime_sizer = wx.BoxSizer(wx.HORIZONTAL)
        #Temp_realtime_sizer.Add(Temp_realtime_label, 0, wx.ALL, 5)
        
        #Right_panel_sizer.Add(Volt_realtime_sizer, 0, wx.ALL|wx.CENTER, 5)
        #Right_panel_sizer.Add(Amp_realtime_sizer, 1, wx.ALL|wx.EXPAND, 5)
        #Right_panel_sizer.Add(Temp_realtime_sizer, 2, wx.ALL|wx.EXPAND, 5)
        
        Overal_sizer.Add(Left_panel_sizer,0, wx.ALL|wx.LEFT, 5)
        #Overal_sizer.Add(Right_panel_sizer,1, wx.ALL|wx.RIGHT, 5)
        
        self.SetSizer(Overal_sizer)
        Overal_sizer.Fit(self)
        self.on_timer()
        self.SerialReader()
    
    def Saving_inputs(self, event):
        TimeValue = self.Time_input.GetValue()
        print TimeValue
        MaxVolt = self.Max_volt_input.GetValue()
        print MaxVolt
        Values_of_PSU.MinVolt = self.Min_volt_input.GetValue()
        print Values_of_PSU.MinVolt
        MinAmp = self.Min_Amp_input.GetValue()
        print MinAmp
        MaxAmp = self.Max_Amp_input.GetValue()
        print MaxAmp
        MinTemp = self.Min_temp_input.GetValue()
        print MinTemp
        MaxTemp = self.Max_temp_input.GetValue()
        print MaxTemp
        event.Skip()

    def on_timer(self):
        countdown = 30
        ser= serial.Serial('COM7', 115200)
        while countdown > 0:
            value_PSU = ser.readline()
            countdown = countdown -1
            nwstuff = value_PSU.split(',')
        self.Serialvalue.SetLabel(str(nwstuff[1]))
        wx.CallLater(1000, self.on_timer)

    def SerialReader(self):
        countdown = 30
        ser= serial.Serial('COM7', 115200)
        
        while countdown > 0:
            value_PSU = ser.readline()
            countdown = countdown -1
            nwstuff = value_PSU.split(',')
            try:
                print nwstuff
                #print nwstuff[0]
                #print nwstuff[1]
                #print nwstuff[2]
                nwstuff[3] = nwstuff[3].replace(';', "")
                #print nwstuff[3]
                #print float(nwstuff[1])
                #print 'Success'
                #print '\n'
                print Values_of_PSU.MinVolt
            except:
                continue


app = wx.App(False)
MainApp(None, "PS Unicorn")
app.MainLoop()
