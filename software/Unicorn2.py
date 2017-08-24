import serial
import wx
import wx.grid as grid
import time
import io
import time

ser = serial.Serial(
    port='COM5',
    baudrate=115200
)

class MainApp(wx.Frame):
    
    def __init__(self, parent, title):
        wx.Frame.__init__(self,parent,title=title)
        self.Show(True)

        self.Panel_1 = Values_of_PSU(self)
        self.Panel_2 =Logic_and_values(self)


        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.Panel_1, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(self.Panel_2, 0, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(sizer)
        self.SetBackgroundColour('#F8F2DA')
        self.Fit ()
        self.Centre()

class Values_of_PSU(wx.Panel):
    MinVolt = 0
    MaxVolt = 0
    MinAmp = 0
    MaxAmp = 0
    MinTemp = 0
    MaxTemp = 0
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent

        font = wx.Font(32, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        font2 = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        font3 = wx.Font(16, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        
        #Buttons, Text controls, widgets, values etc
        Settings_label = wx.StaticText(self, wx.ID_ANY, "Settings")
        Settings_label.SetFont(font)
        Time_label = wx.StaticText(self, wx.ID_ANY, "Time")
        Time_label.SetFont(font2)
        self.Time_input = wx.TextCtrl(self, wx.ID_ANY, "10")

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
        self.Max_temp_input = wx.TextCtrl(self, wx.ID_ANY, "6")
        Start_Stop_button = wx.Button(self, label = "Submit")
        Start_Stop_button.Bind(wx.EVT_BUTTON, self.Saving_inputs)
        
        Start_Stop_button.SetFont(font3)
        Start_Stop_button.SetBackgroundColour('#DDECEF')

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

    def Saving_inputs(self, event):
        Values_of_PSU.TimeValue = self.Time_input.GetValue()
        Values_of_PSU.MaxVolt = self.Max_volt_input.GetValue()
        Values_of_PSU.MinVolt = self.Min_volt_input.GetValue()
        Values_of_PSU.MinAmp = self.Min_Amp_input.GetValue()
        Values_of_PSU.MaxAmp = self.Max_Amp_input.GetValue()
        Values_of_PSU.MinTemp = self.Min_temp_input.GetValue()
        Values_of_PSU.MaxTemp = self.Max_temp_input.GetValue()

class Logic_and_values(wx.Panel):

    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent

        font2 = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        font3 = wx.Font(16, wx.DECORATIVE, wx.NORMAL, wx.BOLD)

        volts_value = wx.StaticText(self, wx.ID_ANY, "Current Volts")
        volts_value.SetFont(font2)
        self.volts_value_update = wx.StaticText(self, wx.ID_ANY, "Serial Volts")
        self.volts_value_update.SetFont(font3)
        Amps_value = wx.StaticText(self, wx.ID_ANY, "Current Amps")
        Amps_value.SetFont(font2)
        self.Amps_value_update = wx.StaticText(self, wx.ID_ANY, "Serial Amps")
        self.Amps_value_update.SetFont(font3)
        Temp_value = wx.StaticText(self, wx.ID_ANY, "Current Temp")
        Temp_value.SetFont(font2)
        self.Temp_value_update = wx.StaticText(self, wx.ID_ANY, "Serial Temp")
        self.Temp_value_update.SetFont(font3)

        Overal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Left_panel_sizer = wx.BoxSizer(wx.VERTICAL)

        Volts_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Volts_sizer.Add(volts_value, 0, wx.ALL, 5)   
        Volts_sizer.Add(self.volts_value_update,0,wx.ALL, 5)

        Amp_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Amp_sizer.Add(Amps_value,0, wx.ALL,5)
        Amp_sizer.Add(self.Amps_value_update,0,wx.ALL, 5)

        Temp_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Temp_sizer.Add(Temp_value,0, wx.ALL,5)
        Temp_sizer.Add(self.Temp_value_update,0,wx.ALL, 5)

        Left_panel_sizer.Add(Volts_sizer,0, wx.ALL|wx.EXPAND ,5)
        Left_panel_sizer.Add(Amp_sizer,0, wx.ALL| wx.EXPAND ,5)
        Left_panel_sizer.Add(Temp_sizer,0, wx.ALL| wx.EXPAND ,5)

        Overal_sizer.Add(Left_panel_sizer,0, wx.ALL|wx.CENTER, 5)
        self.SetSizer(Overal_sizer)
        Overal_sizer.Fit(self)
        self.Centre()

        # ser.open()

        self.on_timer()

    def on_timer(self):
        countdown = 30
        
        while countdown > 0:
            value_PSU = ser.readline()
            countdown = countdown -1
            try:
                nwstuff = value_PSU.split(',')
                nwstuff[3] = nwstuff[3].replace(';',"")
            except:
                continue
        self.volts_value_update.SetLabel(str(nwstuff[1]))
        self.Amps_value_update.SetLabel(str(nwstuff[2]))
        self.Temp_value_update.SetLabel(str(nwstuff[3]))
        wx.CallLater(1000, self.on_timer)

    
app = wx.App(False)
MainApp(None, "PS Unicorn")
app.MainLoop()
