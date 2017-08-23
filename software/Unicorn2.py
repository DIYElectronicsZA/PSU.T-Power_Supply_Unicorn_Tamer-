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
        self.Panel_1 = Values_of_PSU(self)
        self.Panel_2 =Logic_and_values(self)
        self.Panel_2.Hide()
        self.SetBackgroundColour('#F8F2DA')
        self.Fit ()
        self.Centre()

class Values_of_PSU(wx.Panel):
    MinVolt = 0
    
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
        Start_Stop_button.Bind(wx.EVT_BUTTON, self.Switchpanel)
        
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

    def Switchpanel(self,event):
        self.Panel_2 = Logic_and_values(self)
        self.Panel_2.Show()

class Logic_and_values(wx.Frame):
    
    def __init__(self, parent):
        wx.Frame.__init__(self, parent=parent)
        self.frame = parent
        txt = wx.TextCtrl(self)

        Overal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Left_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        Left_panel_sizer.Add(txt,0, wx.ALL ,5)
        Overal_sizer.Add(Left_panel_sizer,0, wx.ALL|wx.LEFT, 5)
        self.Centre()

app = wx.App(False)
MainApp(None, "PS Unicorn")
app.MainLoop()
