from __future__ import print_function
import wx
import serial

import os
from wx.lib.plot import PolyLine, PlotCanvas, PlotGraphics
import wx.grid as grid
import io
import logging
import sys
import glob
import numpy as np
import csv
#import matplotlib.py as plt
from serialfunctions import SerialPort

import threading
from DataObjects import DataObject
from numpy import arange, sin, pi
#matplotlib.use('WXAgg')
#-*- coding: utf-8 -*-

import wx.grid as gridlib
from serialfunctions import SerialPort
from numpy import arange, sin, pi
import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
import matplotlib.patches as mpatches



# matplotlib requires wxPython 2.8+
# set the wxPython version in lib\site-packages\wx.pth file
# or if you have wxversion installed un-comment the lines below
#import wxversion
#wxversion.ensureMinimal('2.8')

import sys
import time
import os
import gc
import matplotlib
matplotlib.use('WXAgg')
import matplotlib.cm as cm
import matplotlib.cbook as cbook
from matplotlib.backends.backend_wxagg import Toolbar, FigureCanvasWxAgg
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import wx
import wx.xrc as xrc
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

ERR_TOL = 1e-5  # floating point slop for peak-detection


matplotlib.rc('image', origin='lower')

########################################################################
class PanelOne(wx.Panel):
    serial_port = SerialPort()
    data_object = DataObject(volts= 0,amps= 0,temp= 0,port=1, Vmax = 0, Vmin = 0, Amax = 0, Amin = 0, Tmax = 0, Tmin = 0)
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        self.blue = 100
        wx.Panel.__init__(self, parent=parent)

        self.fig = Figure((5, 4), 75)
        self.canvas = FigureCanvasWxAgg(self, -1, self.fig)
        self.axes = self.fig.add_subplot(111)
        self.axes.set(title="Power Supply Tester Output", xlabel="Time Elapsed in Seconds (s)", ylabel="Power in Wattage (Watts)")
        chan1_leg = mlines.Line2D([], [],color='green', label='Channel One', marker = 'o')
        chan2_leg = mlines.Line2D([], [],color='blue', label='Channel One', marker = 'x')
        self.axes.legend(loc=4, borderaxespad=0.,handles =[chan1_leg, chan2_leg])
        plot_it = wx.Button(self, wx.ID_ANY, label= "plot that graph")
        plot_it.Bind(wx.EVT_BUTTON, self.plot_it)
        plot_it.Bind(wx.EVT_BUTTON, self.onToggle)        
        # self.toolbar.set_active([0,1])

        self.canvas = FigureCanvas(self, -1, self.fig)
        # Now put all into a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        # This way of adding to sizer allows resizing
        sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        sizer.Add(plot_it, 1, wx.BOTTOM)
        # Best to allow the toolbar to resize!                
        self.SetSizer(sizer)
        self.Fit()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.plot_it, self.timer)
    
    def plot_it(self,event):
        self.plotting()

    def plotting(self):
        
        if UserDisplayPanel.time > 0:
            initial_time = float(UserDisplayPanel.Time_input.GetValue()) *60
            max_power =(float(UserDisplayPanel.Max_volt_input.GetValue()) * float(UserDisplayPanel.Max_Amp_input.GetValue()))
            min_power =(float(UserDisplayPanel.Min_volt_input.GetValue()) * float(UserDisplayPanel.Min_Amp_input.GetValue()))
            current_1 = float(PanelOne.serial_port.amps)
            voltage_1 = float(PanelOne.serial_port.volts)
            current_2 = float(PanelOne.serial_port.amps2)
            voltage_2 = float(PanelOne.serial_port.volts2)
            power_1 = (current_1 * voltage_1)
            power_2 = (current_2 * voltage_2)
            x_axis = (initial_time -float(UserDisplayPanel.time))
            self.axes.axhline(min_power, color='r', linewidth=3, label = "Min Power Output")
            self.axes.axhline(max_power, color='r', linewidth=3, label = "Max Power Output")
            self.axes.plot(x_axis, power_1, "go", label = "Channel One")
            self.axes.plot(x_axis, power_2, "bx", label = "CHannel Two")
            self.canvas.draw()
            x_axis = x_axis + 1
    
    def onToggle(self, event):
        """Timer used to track serial"""
        if self.timer.IsRunning():
            self.timer.Stop()
            self.axes.clear()
            #self.toggleBtn.SetLabel("Start")
            print ("timer stopped!")
        else:
            print ("starting timer...")
            self.timer.Start(1000)
            #self.toggleBtn.SetLabel("Stop")
            self.axes.set(title="Power Supply Tester Output", xlabel="Time Elapsed in Seconds (s)", ylabel="Power in Wattage (Watts)")
            chan1_leg = mlines.Line2D([], [],color='green', label='Channel One', marker = 'o')
            chan2_leg = mlines.Line2D([], [],color='blue', label='Channel One', marker = 'x')
            self.axes.legend(loc=4, borderaxespad=0.,handles =[chan1_leg, chan2_leg])
        event.Skip()            




    # def plotting(self, event):
    #     new_list = []
    #     if len(new_list) < len(PanelOne.data_object.amps_list):
    #         new_list = PanelOne.data_object.amps_list
    #         for values in new_list:
    #             x_axis = float(PanelOne.data_object.amps_list.index(values))
    #             y_axis = float(PanelOne.serial_port.amps)
    #             self.axes.plot(x_axis, y_axis, "ro")
    #             self.canvas.draw()
    #             print (PanelOne.serial_port.amps)
    #             continue
########################################################################
class UserDisplayPanel(wx.Panel):
    """"""
    # Class Variables
    serial_port = SerialPort()
    data_object = DataObject(volts= 0,amps= 0,temp= 0,port=1, Vmax = 0, Vmin = 0, Amax = 0, Amin = 0, Tmax = 0, Tmin = 0)
    port_to_connect = ""
    time = 0
    offset = 0
    offset_2 = 0
    
    

    def __init__(self, parent):
        """Class Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent

        #Different font styles used throughout the display
        font  = wx.Font(34, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
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
        UserDisplayPanel.Time_input = wx.TextCtrl(self, wx.ID_ANY, "10")
        #TODO: Error check, to ensure int is entered

        #Min and Max Voltage label and text control input for parameters in logic
        Min_volt_label = wx.StaticText(self, wx.ID_ANY, "Minimum Voltage  ")
        Min_volt_label.SetFont(font2)
        UserDisplayPanel.Min_volt_input = wx.TextCtrl(self, wx.ID_ANY, "10")

        Max_volt_label = wx.StaticText(self, wx.ID_ANY, "Maximum Voltage  ")
        Max_volt_label.SetFont(font2)
        UserDisplayPanel.Max_volt_input = wx.TextCtrl(self, wx.ID_ANY, "13")
        #TODO: Error check, to ensure int is entered

        #Min and Max Current label and text control input for parameters in logic
        Min_Amp_label = wx.StaticText(self, wx.ID_ANY, "Minimum Current   ")
        Min_Amp_label.SetFont(font2)
        UserDisplayPanel.Min_Amp_input = wx.TextCtrl(self, wx.ID_ANY, "5")

        Max_Amp_label = wx.StaticText(self, wx.ID_ANY, "Maximum Current   ")
        Max_Amp_label.SetFont(font2)
        UserDisplayPanel.Max_Amp_input = wx.TextCtrl(self, wx.ID_ANY, "9")
        #TODO: Error check, to ensure int is entered

        ##Min and Max Temperature label and text control input for parameters in logic
        Min_temp_label = wx.StaticText(self, wx.ID_ANY, "Minimum Temp(C)")
        Min_temp_label.SetFont(font2)
        self.Min_temp_input = wx.TextCtrl(self, wx.ID_ANY, "20")

        Max_temp_label = wx.StaticText(self, wx.ID_ANY, "Maximum Temp(C)")
        Max_temp_label.SetFont(font2)
        self.Max_temp_input = wx.TextCtrl(self, wx.ID_ANY, "60")

        #Start/Stop button to start or end the program
        #Start_Stop_button = wx.Button(self, label = "Submit")
        #Start_Stop_button.Bind(wx.EVT_BUTTON, self.update_range_values)
        #Start_Stop_button.SetForegroundColour(wx.Colour(245,245,245))
        #Start_Stop_button.SetFont(font3)
        #Start_Stop_button.SetBackgroundColour('#000000')

        #Labels, combobox and button for selecting port
        Ports = wx.StaticText(self, wx.ID_ANY, "Available Ports") #Label for available ports
        Ports.SetFont(font2)
        self.Port_dropdown = wx.ComboBox(self, wx.ID_ANY) #ComboBox
        port_refresh = wx.Button(self, wx.ID_ANY, label= "Refresh ports") #Refresh port button
        port_refresh.Bind(wx.EVT_BUTTON, self.refresh_dropdown)
        Select_port = wx.Button(self, wx.ID_ANY, label = 'Connect to port') #Select port button
        Select_port.Bind(wx.EVT_BUTTON, self.select_port)
        Refresh_all = wx.Button(self, wx.ID_ANY, label = "Refresh values")
        Refresh_all.Bind(wx.EVT_BUTTON,self.ClearAll)

        Select_port.Bind(wx.EVT_BUTTON, self.onToggle)
        Disconnect_port = wx.Button(self, wx.ID_ANY, label = "Disconnect")
        Disconnect_port.Bind(wx.EVT_BUTTON, self.stop_serial) #Disconnect from serial port
        Disconnect_port.Bind(wx.EVT_BUTTON, self.onToggle)
        self.port_select_error = wx.StaticText(self, wx.ID_ANY, "") #Text area to display Port seletion error
        self.port_select_error.SetFont(font2)
        Amp_offset_1 = wx.Button(self, wx.ID_ANY, label= "Ch1 amps offset reset") #Refresh port button
        Amp_offset_1.Bind(wx.EVT_BUTTON, self.refresh_amps)
        Amp_offset_2 = wx.Button(self, wx.ID_ANY, label= "Ch2 amps offset reset") #Refresh port button
        Amp_offset_2.Bind(wx.EVT_BUTTON, self.refresh_amps_2)
        #Amp_value = wx.StaticText(self, wx.ID_ANY, "0")
        #Labels and values to update via logic for the current volt, current and temperature
        error_marker = wx.StaticText(self, wx.ID_ANY, "Number of errors: ")
        self.error_marker_update = wx.StaticText(self, wx.ID_ANY, "000")
        error_marker.SetFont(font2)
        self.error_marker_update2 = wx.StaticText(self, wx.ID_ANY, "")
        self.error_marker_update.SetFont(font3)
        self.error_marker_update2.SetFont(font3)
        time_left = wx.StaticText(self, wx.ID_ANY, "Time left: ")
        self.time_left_update = wx.StaticText(self, wx.ID_ANY, "0:00")
        time_left.SetFont(font2)
        self.time_left_update.SetFont(font2)
        volts_value = wx.StaticText(self, wx.ID_ANY, "Current Volts:")
        volts_value.SetFont(font2)
        self.volts_value_update = wx.StaticText(self, wx.ID_ANY, "Serial Volts")
        self.volts_value_update_2 = wx.StaticText(self, wx.ID_ANY, "Serial Volts 2")
        self.volts_value_update.SetFont(font3)
        self.volts_value_update_2.SetFont(font3)
        self.volts_value_update.SetForegroundColour(wx.Colour(153,17,37))
        self.volts_value_update_2.SetForegroundColour(wx.Colour(153,17,37))
        Amps_value = wx.StaticText(self, wx.ID_ANY, "Current Amps:")
        Amps_value.SetFont(font2)
        self.Amps_value_update = wx.StaticText(self, wx.ID_ANY, "Serial Amps")
        self.Amps_value_update_2 = wx.StaticText(self, wx.ID_ANY, "Serial Amps 2")
        self.Amps_value_update.SetFont(font3)
        self.Amps_value_update_2.SetFont(font3)
        self.Amps_value_update.SetForegroundColour(wx.Colour(153,17,37))
        self.Amps_value_update_2.SetForegroundColour(wx.Colour(153,17,37))
        Temp_value = wx.StaticText(self, wx.ID_ANY, "Current Temp:")
        Temp_value.SetFont(font2)
        self.Temp_value_update = wx.StaticText(self, wx.ID_ANY, "Serial Temp")
        self.Temp_value_update_2 = wx.StaticText(self, wx.ID_ANY, "Serial Temp 2")
        self.Temp_value_update.SetFont(font3)
        self.Temp_value_update_2.SetFont(font3)
        self.Temp_value_update.SetForegroundColour(wx.Colour(153,17,37))
        self.Temp_value_update_2.SetForegroundColour(wx.Colour(153,17,37))
        Power_value = wx.StaticText(self, wx.ID_ANY, "Current Power: ")
        Power_value.SetFont(font2)
        self.power_value_update = wx.StaticText(self, wx.ID_ANY, "Power Output")
        self.power_value_update_2 = wx.StaticText(self, wx.ID_ANY, "Power Output 2")
        self.power_value_update_2.SetFont(font3)
        self.power_value_update.SetFont(font3)
        self.power_value_update.SetForegroundColour(wx.Colour(153,17,37))
        self.power_value_update_2.SetForegroundColour(wx.Colour(153,17,37))
        self.volt_range = wx.StaticText(self, wx.ID_ANY, "                      ")
        self.power_range = wx.StaticText(self, wx.ID_ANY, "                      ")
        self.volt_range.SetFont(font2)
        self.power_range.SetFont(font2)
        self.amp_range = wx.StaticText(self, wx.ID_ANY, "                      ")
        self.amp_range.SetFont(font2)
        self.temp_range = wx.StaticText(self, wx.ID_ANY, "                      ")
        self.temp_range.SetFont(font2)
        self.volt_range_2 = wx.StaticText(self, wx.ID_ANY, "                      ")
        self.power_range_2 = wx.StaticText(self, wx.ID_ANY, "                      ")
        self.volt_range_2.SetFont(font2)
        self.power_range_2.SetFont(font2)
        self.amp_range_2 = wx.StaticText(self, wx.ID_ANY, "                      ")
        self.amp_range_2.SetFont(font2)
        self.temp_range_2 = wx.StaticText(self, wx.ID_ANY, "                      ")
        self.temp_range_2.SetFont(font2)
        self.Bind(wx.EVT_CLOSE, self.stop_serial)
        self.Bind(wx.EVT_CLOSE, self.onExit)

        self.pass_fail = wx.StaticText(self, wx.ID_ANY, "Pass")
        self.pass_fail.SetForegroundColour((0,100,0))
        self.pass_fail.SetFont(font2)        

        #Sizers used to insert widgets

        Overal_sizer       = wx.BoxSizer(wx.VERTICAL)
        Overal_sizer_2       = wx.BoxSizer(wx.VERTICAL)
        Top_panel_sizer    = wx.BoxSizer(wx.VERTICAL) #Sizer for top half of overall sizer
        Bottom_panel_sizer = wx.BoxSizer(wx.VERTICAL) #Sizer for Bottom half of overall sizer
        
        #Setting sizer
        Setting_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Setting_sizer.Add(Settings_label,0, wx.ALL, 5)
        
        #Time input sizer
        threshold_sizer = wx.BoxSizer(wx.VERTICAL)
        threshold_sizer.Add(self.pass_fail, 0, wx.ALL, 5)
        time_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        time_input_sizer.Add(Time_label, 0, wx.ALL,5)
        time_input_sizer.Add(self.Time_input,0, wx.ALL, 5)

        #Voltage input sizer
        Volt_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Volt_input_sizer.Add(Min_volt_label,0, wx.ALL, 5)
        Volt_input_sizer.Add(UserDisplayPanel.Min_volt_input,0, wx.ALL, 5)
        Volt_input_sizer.Add(Max_volt_label,0, wx.ALL, 5)
        Volt_input_sizer.Add(UserDisplayPanel.Max_volt_input,0, wx.ALL, 5)
        
        #Current input sizer
        Amp_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Amp_input_sizer.Add(Min_Amp_label, 0, wx.ALL, 5)
        Amp_input_sizer.Add(UserDisplayPanel.Min_Amp_input, 0, wx.ALL, 5)
        Amp_input_sizer.Add(Max_Amp_label, 0, wx.ALL, 5)
        Amp_input_sizer.Add(UserDisplayPanel.Max_Amp_input, 0, wx.ALL, 5)
        
        #Temperature input sizer
        Temp_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Temp_input_sizer.Add(Min_temp_label, 0, wx.ALL, 5)
        Temp_input_sizer.Add(self.Min_temp_input, 0, wx.ALL, 5)
        Temp_input_sizer.Add(Max_temp_label, 0, wx.ALL, 5)
        Temp_input_sizer.Add(self.Max_temp_input, 0, wx.ALL, 5)
        
        #Start/stop sizer
        Start_stop_sizer = wx.BoxSizer(wx.HORIZONTAL)
        #Start_stop_sizer.Add(Start_Stop_button, 0, wx.ALL,5)
        
        #Adding Setting, time, voltage, current, temperature inputs into TOP panel
        Top_panel_sizer.Add(Setting_sizer, 0, wx.ALL|wx.CENTER, 5)
        Top_panel_sizer.Add(time_input_sizer, 0, wx.ALL|wx.EXPAND, 5)
        Top_panel_sizer.Add(Volt_input_sizer, 0, wx.ALL|wx.EXPAND, 5)
        Top_panel_sizer.Add(Amp_input_sizer, 0, wx.ALL|wx.EXPAND, 5)
        Top_panel_sizer.Add(Temp_input_sizer, 0, wx.ALL|wx.EXPAND, 5)
        Top_panel_sizer.Add(Start_stop_sizer, 0, wx.ALL|wx.CENTER, 5)

        #Ports sizer
        ports_sizer = wx.BoxSizer(wx.HORIZONTAL)
        offset_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ports_sizer.Add(Ports, 0, wx.ALL, 5)
        ports_sizer.Add(self.Port_dropdown, 0, wx.ALL, 5)
        ports_sizer.Add(Select_port, 0 , wx.ALL, 5)
        ports_sizer.Add(port_refresh, 0, wx.ALL, 5)
        ports_sizer.Add(Disconnect_port, 0, wx.ALL, 5)
        ports_sizer.Add(Refresh_all, 0, wx.ALL,5)

        offset_sizer.Add(Amp_offset_1, 0, wx.ALL, 5)
        offset_sizer.Add(Amp_offset_2, 0, wx.ALL, 5)
        
        ports_selection_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ports_selection_sizer.Add(self.port_select_error,0, wx.ALL,5)

        #Volt display sizer
        Volts_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Volts_sizer.Add(volts_value, 0, wx.ALL, 5)   
        Volts_sizer.Add(self.volts_value_update,0,wx.ALL, 5)
        Volts_sizer.Add(self.volt_range,0, wx.ALL,5)
        Volts_sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        Volts_sizer_2.Add(self.volts_value_update_2,0,wx.ALL, 5)
        Volts_sizer_2.Add(self.volt_range_2,0, wx.ALL,5)

        #Amp display sizer
        Amp_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Amp_sizer.Add(Amps_value, 0, wx.ALL, 5)
        Amp_sizer.Add(self.Amps_value_update,0,wx.ALL, 5)
        Amp_sizer.Add(self.amp_range,0, wx.ALL,5)
        Amp_sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        Amp_sizer_2.Add(self.Amps_value_update_2,0,wx.ALL, 5)
        Amp_sizer_2.Add(self.amp_range_2,0,wx.ALL, 5)

        #Temp display sizer
        Temp_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Temp_sizer.Add(Temp_value, 0, wx.ALL, 5)
        Temp_sizer.Add(self.Temp_value_update, 0,wx.ALL, 5)
        Temp_sizer.Add(self.temp_range,0, wx.ALL,5)
        Temp_sizer_2= wx.BoxSizer(wx.HORIZONTAL)
        Temp_sizer_2.Add(self.Temp_value_update_2,0,wx.ALL, 5)
        Temp_sizer_2.Add(self.temp_range_2,0, wx.ALL,5)

        #power display sizer
        power_sizer = wx.BoxSizer(wx.HORIZONTAL)
        power_sizer.Add(Power_value, 0 , wx.ALL, 5)
        power_sizer.Add(self.power_value_update,0 , wx.ALL, 5)
        power_sizer.Add(self.power_range,0 , wx.ALL, 5)
        power_sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        power_sizer_2.Add(self.power_value_update_2,0,wx.ALL, 5)
        power_sizer_2.Add(self.power_range_2,0,wx.ALL, 5)

        #Time sizer
        time_sizer = wx.BoxSizer(wx.HORIZONTAL)
        time_sizer.Add(time_left,0, wx.ALL,5)
        time_sizer.Add(self.time_left_update,0, wx.ALL,5)

        #Error marker sizer
        error_sizer = wx.BoxSizer(wx.HORIZONTAL)
        error_sizer.Add(error_marker, 0, wx.ALL, 5)
        error_sizer.Add(self.error_marker_update,0, wx.ALL,5)
        error_sizer.Add(threshold_sizer,0, wx.ALL,5)


        #Channel 1 volts, amps, temp, power values sizer
        channel1_sizer = wx.BoxSizer(wx.VERTICAL)
        channel1_sizer.Add(time_sizer, 0 ,wx.ALL|wx.EXPAND,5)
        channel1_sizer.Add(error_sizer, 0 ,wx.ALL|wx.EXPAND,5)
        channel1_sizer.Add(Volts_sizer, 0, wx.ALL|wx.EXPAND, 5)
        channel1_sizer.Add(Amp_sizer,0, wx.ALL|wx.EXPAND,5)
        channel1_sizer.Add(Temp_sizer,0, wx.ALL|wx.EXPAND,5)
        channel1_sizer.Add(power_sizer,0 , wx.ALL|wx.EXPAND,5)

        #Error marker sizer 2
        error_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        error_sizer2.Add(self.error_marker_update2,0, wx.ALL,5)

        #Channel 2 sizer
        channel2_sizer = wx.BoxSizer(wx.VERTICAL)
        channel2_sizer.Add(error_sizer2,0, wx.ALL,5)
        channel2_sizer.Add(error_sizer2,0, wx.ALL,5)
        channel2_sizer.Add(Volts_sizer_2, 0, wx.ALL, 5)
        channel2_sizer.Add(Amp_sizer_2,0, wx.ALL,5)
        channel2_sizer.Add(Temp_sizer_2,0, wx.ALL,5)
        channel2_sizer.Add(power_sizer_2,0, wx.ALL,5)    
        #Adding Ports components, Volt display, Amp display and Temp display to BOTTOM Panel
        combo_channel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        breaker_sizer = wx.BoxSizer(wx.VERTICAL)
        
        combo_channel_sizer.Add(channel1_sizer,0,wx.ALL|wx.EXPAND,5)
        combo_channel_sizer.Add(channel2_sizer, 0, wx.ALL|wx.EXPAND,5)
        Bottom_panel_sizer.Add(ports_sizer, 0, wx.ALL|wx.EXPAND,5)
        Bottom_panel_sizer.Add(offset_sizer, 0, wx.ALL|wx.EXPAND,5)
        Bottom_panel_sizer.Add(ports_selection_sizer, 0, wx.CENTER,5)
        Bottom_panel_sizer.Add(combo_channel_sizer,0, wx.ALL|wx.EXPAND,5)

        #Adding Top and Bottom sizers to the overall sizer
        Overal_sizer.Add(Top_panel_sizer,    0, wx.ALL|wx.CENTER, 5)
        Overal_sizer.Add(Bottom_panel_sizer, 0, wx.ALL|wx.CENTER, 5)
        #Overal_sizer_2.Add(, 0, wx.ALL|wx.CENTER, 5)
        Main_sizer = wx.BoxSizer(wx.VERTICAL)
        Main_sizer.Add(Overal_sizer,   0, wx.CENTER, 5)
        Main_sizer.Add(Overal_sizer_2, 0, wx.CENTER, 5)
        #setup serial ports list: 
        self.refresh_dropdown(self)

        #messing around with timers https://www.blog.pythonlibrary.org/2009/08/25/wxpython-using-wx-timers/
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
 
        #self.toggleBtn = wx.Button(self, wx.ID_ANY, "Start")
        #self.toggleBtn.Bind(wx.EVT_BUTTON, self.onToggle)

        self.SetSizer(Main_sizer)
        Main_sizer.Fit(self)
        self.Centre()

     # Function to stop serial when "x" is clicked
    def ClearAll(self, event):
        #Update for volts value
        self.volts_value_update.SetLabel(" 0 V")
        #Update for Amp value
        self.Amps_value_update.SetLabel(" 0 A")
        self.Amps_value_update_2.SetLabel("0 A")
        #Update for Temp value
        self.Temp_value_update.SetLabel("0" + u"\N{DEGREE SIGN}" + "C")
        #Update power value
        self.power_value_update_2.SetLabel("0 W")
        #Update of range values
        #Update for volts value
        self.volts_value_update_2.SetLabel("0 V")
        #Update for Amp value
        #Update for Temp value
        self.Temp_value_update_2.SetLabel(" 0" + u"\N{DEGREE SIGN}" +  "C")
        self.power_value_update.SetLabel("0 W")
        self.error_marker_update.SetLabel("0")
        self.pass_fail.SetForegroundColour((0,100,0))
        self.pass_fail.SetLabel("PASS")
        self.volt_range.SetLabel("")
        self.amp_range.SetLabel("")
        self.temp_range.SetLabel("")
        self.power_range.SetLabel(
            "")
        self.volt_range_2.SetLabel("")
        self.amp_range_2.SetLabel("")
        self.temp_range_2.SetLabel("")
        self.power_range_2.SetLabel("")
        #self.temp_range.SetLabel(UserDisplayPanel.data_object.checkerrorvoltage.temp_ranges)
        self.time_left_update.SetLabel("0")
        self.port_select_error.SetLabel("Disconnected")
        UserDisplayPanel.serial_port.close_serial()
        UserDisplayPanel.time = 0
        self.time_left_update.SetLabel("0:00")
        return UserDisplayPanel.update_serial_display
        return UserDisplayPanel.update     


    def onExit(self, event):
        sys.exit()
        self.Close()
  
    def on_close(self, event):
        UserDisplayPanel.read_serial.exit()
  
    def refresh_dropdown(self,event):
        ''' Method to refresh the list showing in the combobox found in the Bottom Panel in UserDisplayPanel ''' 
        
        # Clear the comports list: 
        self.Port_dropdown.Clear()
        # Add the new comports
        
        new_list = UserDisplayPanel.serial_port.serial_ports_list()
        self.Port_dropdown.Append(new_list)

    def select_port(self,event):
        """Method to connect to a User selected port, ifelse statement to ensure a port is selected"""
        #t = Timer(10.0, self.port_select_error.SetLabel("") )
        UserDisplayPanel.port_to_connect = self.Port_dropdown.GetValue() #Get Value from the ComboBox
        if len(UserDisplayPanel.port_to_connect) < 1:
            self.port_select_error.SetLabel("No port selected")  
        else:
            UserDisplayPanel.serial_port.port_to_open = UserDisplayPanel.port_to_connect #Run Opening Port from Serialfunctions.py document
            UserDisplayPanel.serial_port.serial_port_open(UserDisplayPanel.port_to_connect)     
            self.port_select_error.SetLabel("Port opened")
            #self.update_serial_display() 
            self.read_serial()
            UserDisplayPanel.time =UserDisplayPanel.Time_input.GetValue()
            UserDisplayPanel.time = int(UserDisplayPanel.time)
            UserDisplayPanel.time = UserDisplayPanel.time * 60
        event.Skip()

    def get_range_values(self):
        """continously update ranges in channels, stating whether out of range or in range."""

        Vmax_input = int(UserDisplayPanel.Max_volt_input.GetValue())
        Vmin_input = int(UserDisplayPanel.Min_volt_input.GetValue())
        Amax_input = int(UserDisplayPanel.Max_Amp_input.GetValue())
        Amin_input = int(UserDisplayPanel.Min_Amp_input.GetValue())
        Tmax_input = int(self.Max_temp_input.GetValue())
        Tmin_input = int(self.Min_temp_input.GetValue())

        UserDisplayPanel.time = int(UserDisplayPanel.time) - 1
        try:
            print (UserDisplayPanel.time)
        except: pass
        self.power_1 = UserDisplayPanel.data_object.calculatepower(volts =UserDisplayPanel.serial_port.volts, amps = UserDisplayPanel.serial_port.amps)
        UserDisplayPanel.data_object.checkerrorvoltage(volts =UserDisplayPanel.serial_port.volts, volt_ranges= "", Vmax = Vmax_input, Vmin = Vmin_input)
        UserDisplayPanel.data_object.checkerrorcurrent(amps= UserDisplayPanel.serial_port.amps, amps_ranges= "", Amax = Amax_input, Amin = Amin_input, offset = UserDisplayPanel.offset)
        UserDisplayPanel.data_object.checkerrortemp(temp = UserDisplayPanel.serial_port.temp, temp_ranges= "", Tmax = Tmax_input, Tmin = Tmin_input)

        UserDisplayPanel.data_object.make_list(volts =UserDisplayPanel.serial_port.volts, amps = UserDisplayPanel.serial_port.amps )
        
        self.power_2 = UserDisplayPanel.data_object.calculatepower(volts =UserDisplayPanel.serial_port.volts2, amps = UserDisplayPanel.serial_port.amps2)
        UserDisplayPanel.data_object.checkerrorvoltage(volts =UserDisplayPanel.serial_port.volts2, volt_ranges= "", Vmax = Vmax_input, Vmin = Vmin_input)
        UserDisplayPanel.data_object.checkerrorcurrent(amps = UserDisplayPanel.serial_port.amps2, amps_ranges= "", Amax = Amax_input, Amin = Amin_input, offset = UserDisplayPanel.offset_2)

    def read_serial(self):
        """Function to start serial_data function in serialfunctions"""
        t = threading.Thread(target=UserDisplayPanel.serial_port.serial_data) 
        t.start()

    def update_serial_display(self):
        if UserDisplayPanel.time > 0:
            """Function to update bottom panel display to current serial values"""
            #Update for volts value
            self.volts_value_update.SetLabel(UserDisplayPanel.serial_port.volts + " V")
            #Update for Amp value
            Amp_to_d = (float(UserDisplayPanel.serial_port.amps) - float(UserDisplayPanel.offset))
            Amp_to_d_2 = (float(UserDisplayPanel.serial_port.amps2) - float(UserDisplayPanel.offset_2))
            self.Amps_value_update.SetLabel(str(Amp_to_d) + " A")
            self.Amps_value_update_2.SetLabel(str(Amp_to_d_2) + " A")
            #Update for Temp value
            self.Temp_value_update.SetLabel(UserDisplayPanel.serial_port.temp + u"\N{DEGREE SIGN}" + "C")
            #Update power value
            self.power_value_update_2.SetLabel(self.power_2)
            #Update of range values
            #Update for volts value
            self.volts_value_update_2.SetLabel(UserDisplayPanel.serial_port.volts2 + " V")
            #Update for Amp value
            self.Amps_value_update_2.SetLabel(UserDisplayPanel.serial_port.amps2 + " A")
            #Update for Temp value
            self.Temp_value_update_2.SetLabel(UserDisplayPanel.serial_port.temp2 + u"\N{DEGREE SIGN}" + "C")
            self.power_value_update.SetLabel(self.power_1)
            self.error_marker_update.SetLabel(str(UserDisplayPanel.data_object.error_marker))
            if int(UserDisplayPanel.data_object.error_marker) > 10:
                self.pass_fail.SetForegroundColour((255,0,0))
                self.pass_fail.SetLabel("Fail")
            self.volt_range.SetLabel(UserDisplayPanel.data_object.volt_ranges)
            self.amp_range.SetLabel(UserDisplayPanel.data_object.amps_ranges)
            self.temp_range.SetLabel(UserDisplayPanel.data_object.temp_ranges)
            self.power_range.SetLabel(UserDisplayPanel.data_object.power_ranges)
            self.volt_range_2.SetLabel(UserDisplayPanel.data_object.volt_ranges)
            self.amp_range_2.SetLabel(UserDisplayPanel.data_object.amps_ranges)
            self.temp_range_2.SetLabel(UserDisplayPanel.data_object.temp_ranges)
            self.power_range_2.SetLabel(UserDisplayPanel.data_object.power_ranges)
            #self.temp_range.SetLabel(UserDisplayPanel.data_object.checkerrorvoltage.temp_ranges)
            minutes, seconds= divmod(UserDisplayPanel.time, 60)
            self.time_left_update.SetLabel(str(minutes) + ":" + str(seconds))     
    
    def stop_serial(self,event):
        """function to stop serial connection"""
        UserDisplayPanel.serial_port.close_serial()
        UserDisplayPanel.time = 0
        self.time_left_update.SetLabel("0:00")
        return UserDisplayPanel.update_serial_display
        return UserDisplayPanel.update

        event.Skip()

    def onToggle(self, event):
        """Timer used to track serial"""
        if self.timer.IsRunning():
            self.timer.Stop()

            #self.toggleBtn.SetLabel("Start")
            print ("timer stopped!")
        else:
            print ("starting timer...")
            self.timer.Start(1000)
            #self.toggleBtn.SetLabel("Stop")
        event.Skip()

    def update(self, event):
        print ("\nupdated: ",)
        #print time.ctime()
        self.get_range_values()
        self.update_serial_display()
        #self.update_range_values()

    def refresh_amps(self,event):
        UserDisplayPanel.offset = UserDisplayPanel.serial_port.amps
        #self.offset = int(offset)
        #print UserDisplayPanel.offset
        event.Skip()

    def refresh_amps_2(self,event):
        UserDisplayPanel.offset_2 = UserDisplayPanel.serial_port.amps2
        #self.offset = int(offset)
        #print UserDisplayPanel.offset
        event.Skip()

    def saving_serial(self,event):
        self.currentDirectory = os.getcwd()
        
        with open('Power_supply_tester_errors.csv', 'w') as csvfile:
            fieldnames = ['Channel','Test number', 'Voltage', 'Current', 'Temperature', 'Point of error']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            max_volt = UserDisplayPanel.Max_volt_input.GetValue()
            min_volt = UserDisplayPanel.Min_volt_input.GetValue()
            max_amp = UserDisplayPanel.Max_Amp_input.GetValue()
            min_amp = UserDisplayPanel.Min_Amp_input.GetValue()
            max_temp = self.Max_temp_input.GetValue()
            min_temp = self.Min_temp_input.GetValue()
        
            for values in SerialPort.Serial_dict:
                volt = int(values[1])
                amp = int(values[2])
                temp = int(values[3])
                if min_volt > volt or max_volt < volt:
                    writer.writerow({'Channel': values[0][0], 'Test number': values[0][0:], 'Voltage': values[1], 'Current': values[2], 'Temperature': values[3], 'Point of error': 'Voltage'})
                if min_amp > amp or max_amp < amp:
                    writer.writerow({'Channel': values[0][0], 'Test number': values[0][0:], 'Voltage': values[1], 'Current': values[2], 'Temperature': values[3], 'Point of error': 'Current'})
                if min_temp > temp or max_temp < temp:
                    writer.writerow({'Channel': values[0][0], 'Test number': values[0][0:], 'Voltage': values[1], 'Current': values[2], 'Temperature': values[3], 'Point of error': 'Temperature'})


            for values in SerialPort.Serial_dict_2:
                volt = int(values[1])
                amp = int(values[2])
                temp = int(values[3])
                if min_volt > volt or max_volt < volt:
                    writer.writerow({'Channel': values[0][0], 'Test number': values[0][0:], 'Voltage': values[1], 'Current': values[2], 'Temperature': values[3], 'Point of error': 'Voltage'})
                if min_amp > amp or max_amp < amp:
                    writer.writerow({'Channel': values[0][0], 'Test number': values[0][0:], 'Voltage': values[1], 'Current': values[2], 'Temperature': values[3], 'Point of error': 'Current'})
                if min_temp > temp or max_temp < temp:
                    writer.writerow({'Channel': values[0][0], 'Test number': values[0][0:], 'Voltage': values[1], 'Current': values[2], 'Temperature': values[3], 'Point of error': 'Temperature'})
            csvfile.close()

        with open('Power_supply_tester_Results.csv', 'w') as csvfile:
            fieldnames = ['Channel','Test number', 'Voltage', 'Current', 'Temperature']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for values in SerialPort.Serial_dict:
                writer.writerow({'Channel': values[0][0], 'Test number': values[0][0:], 'Voltage': values[1], 'Current': values[2], 'Temperature': values[3]})
            for values in SerialPort.Serial_dict_2:
                writer.writerow({'Channel': values[0][0],'Test number': values[0][0:], 'Voltage': values[1], 'Current': values[2], 'Temperature': values[3]})
            csvfile.close()

 
 
########################################################################
class MyForm(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, 
                          "Panel Switcher Tutorial")
 
        self.panel_one = PanelOne(self)
        self.panel_two = UserDisplayPanel(self)
        self.panel_one.Hide()
 
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_one, 1, wx.EXPAND)
        self.sizer.Add(self.panel_two, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
  
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        switch_panels_menu_item = fileMenu.Append(wx.ID_ANY, 
                                                  "Switch Panels", 
                                                  "Some text")
        self.Bind(wx.EVT_MENU, self.onSwitchPanels, 
                  switch_panels_menu_item)
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
    #----------------------------------------------------------------------
    def onSwitchPanels(self, event):
        """"""
        if self.panel_one.IsShown():
            self.SetTitle("Panel Two Showing")
            self.panel_one.Hide()
            self.panel_two.Show()
        else:
            self.SetTitle("Panel One Showing")
            self.panel_one.Show()
            self.panel_two.Hide()
        self.Layout()
 
 
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()