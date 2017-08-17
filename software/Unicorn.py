import serial
import wx
import wx.grid as grid
import time

class MainApp(wx.Frame):
	def __init__(self,parent,title):
		wx.Frame.__init__(self,parent,title=title, size=(1000,1000))
		self.Show(True)
		self.Panel = Values_of_PSU(self)
		self.Fit()
		
class Values_of_PSU(wx.Panel):
    def __init__(self, parent):
		wx.Panel.__init__(self, parent=parent)
		self.frame = parent
		
		#Buttons, Text controls, widgets, values etc
		
		Settings_label = wx.StaticText(self, wx.ID_ANY, "Settings")
		Time_label = wx.StaticText(self, wx.ID_ANY, "Time")
		Reset_button = wx.Button(self, label= "Reset values")
		#Countdown_value = 
		Min_volt_label = wx.StaticText(self, wx.ID_ANY, "Minimum Voltage threshold")
		Max_volt_label = wx.StaticText(self, wx.ID_ANY, "Maximum Voltage threshold")
		Min_Amp_label = wx.StaticText(self, wx.ID_ANY, "Minimum Current threshold")
		Max_Amp_label = wx.StaticText(self, wx.ID_ANY, "Maximum Current threshold")
		Min_temp_label = wx.StaticText(self, wx.ID_ANY, "Minimum Temperature threshold")
		Max_temp_label = wx.StaticText(self, wx.ID_ANY, "Maximum Temperature threshold")
		Start_Stop_button = wx.Button(self, label = "Start/Stop")
		
		Voltage_realtime_label = wx.StaticText(self, wx.ID_ANY, "Volts")
		Amp_realtime_label = wx.StaticText(self, wx.ID_ANY, "Amps")
		Temp_realtime_label = wx.StaticText(self, wx.ID_ANY, "Temp")
		#Volts_graph =
		#Amp_graph =
		#Temp_graph =
		
		#Layout
		
		Overal_sizer = wx.BoxSizer(wx.VERTICAL)
		Left_panel_sizer = wx.BoxSizer(wx.VERTICAL)
		Right_panel_sizer = wx.BoxSizer(wx.VERTICAL)
		
		Setting_sizer = wx.BoxSizer(wx.HORIZONTAL)
		Setting_sizer.Add(Settings_label,0, wx.ALL, 5)
		
		time_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
		time_input_sizer.Add(Time_label, 0, wx.ALL,5)
		time_input_sizer.Add(Reset_button, 1, wx.ALL, 5)
		
		Volt_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
		Volt_input_sizer.Add(Min_volt_label, 0, wx.ALL, 5)
		Volt_input_sizer.Add(Max_volt_label, 2, wx.ALL, 5)
		
		Amp_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
		Amp_input_sizer.Add(Min_Amp_label, 0, wx.ALL, 5)
		Amp_input_sizer.Add(Max_Amp_label, 2, wx.ALL, 5)
		
		Temp_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
		Temp_input_sizer.Add(Min_temp_label, 0, wx.ALL, 5)
		Temp_input_sizer.Add(Max_temp_label, 2, wx.ALL, 5)
		
		Start_stop_sizer = wx.BoxSizer(wx.HORIZONTAL)
		Start_stop_sizer.Add(Start_Stop_button, 0, wx.ALL,5)
		
		Left_panel_sizer.Add(Setting_sizer, 0, wx.ALL|wx.CENTER, 5)
		Left_panel_sizer.Add(time_input_sizer, 1, wx.ALL|wx.EXPAND, 5)
		Left_panel_sizer.Add(Volt_input_sizer, 2, wx.ALL|wx.EXPAND, 5)
		Left_panel_sizer.Add(Amp_input_sizer, 3, wx.ALL|wx.EXPAND, 5)
		Left_panel_sizer.Add(Temp_input_sizer, 4, wx.ALL|wx.EXPAND, 5)
		Left_panel_sizer.Add(Start_stop_sizer, 5, wx.ALL|wx.CENTER, 5)
		
		Volt_realtime_sizer = wx.BoxSizer(wx.HORIZONTAL)
		Volt_realtime_sizer.Add(Voltage_realtime_label, 0, wx.ALL, 5)
		
		Amp_realtime_sizer = wx.BoxSizer(wx.HORIZONTAL)
		Amp_realtime_sizer.Add(Amp_realtime_label, 0, wx.ALL, 5)
		
		Temp_realtime_sizer = wx.BoxSizer(wx.HORIZONTAL)
		Temp_realtime_sizer.Add(Temp_realtime_label, 0, wx.ALL, 5)
		
		Right_panel_sizer.Add(Volt_realtime_sizer, 0, wx.ALL|wx.EXPAND, 5)
		Right_panel_sizer.Add(Amp_realtime_sizer, 1, wx.ALL|wx.EXPAND, 5)
		Right_panel_sizer.Add(Temp_realtime_sizer, 2, wx.ALL|wx.EXPAND, 5)
		
		Overal_sizer.Add(Left_panel_sizer, 0, wx.ALL|wx.LEFT, 5)
		Overal_sizer.Add(Right_panel_sizer, 1, wx.ALL|wx.RIGHT, 5)
		
		self.SetSizer(Overal_sizer)
		Overal_sizer.Fit(self)
		


app = wx.App(False)
frame = MainApp(None, "PS Unicorn")
app.MainLoop()