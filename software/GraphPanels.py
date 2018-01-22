import serial
import wx
import wx.grid as grid
import time
import io
import time
import logging
import sys
import glob
import numpy as np
#import matplotlib.py as plt
from serialfunctions import SerialPort
import threading
from DataObjects import DataObject
from numpy import arange, sin, pi
import matplotlib.pyplot as plt
#matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
#-*- coding: utf-8 -*-

class GraphPanel(wx.Panel, object):
    """Panel to show graph 1"""
    serial_port = SerialPort()
    plt.ion()

    def __init__(self, parent):
        """Class Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent

        self.figure = Figure() #establishes 
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()
        voltage1 = GraphPanel.serial_port.volts
        voltage2 = GraphPanel.serial_port.volts2
        #while True:
        #    try:
        def plotgraph(self):
            try:
                self.axes.plot(voltage1,voltage2, 'ro')
                plt.pause(0.5)
            except:
                print "ew"

class GraphPanel_2(wx.Panel):
    """Panel to show graph 2"""
    def __init__(self, parent):
        """Class Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

        current1 = GraphPanel.serial_port.amps
        current2 = GraphPanel.serial_port.amps2
        self.axes.plot(current1,current2, 'ro')