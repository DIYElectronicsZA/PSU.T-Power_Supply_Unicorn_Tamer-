import wx
from wx.lib.plot import PolyLine, PlotCanvas, PlotGraphics
import serial
import os
import wx.grid as grid
import time
import io
import time
import logging
import sys
import glob
import numpy as np
import csv
#import matplotlib.py as plt



import threading
from numpy import arange, sin, pi
import matplotlib.pyplot as plt
#matplotlib.use('WXAgg')
#-*- coding: utf-8 -*-
import numpy as np


class PanelOne(wx.Panel):
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent
        # create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        checkSizer = wx.BoxSizer(wx.HORIZONTAL)
 
        # create the widgets
        self.canvas = PlotCanvas(self)
        self.canvas.Draw(drawBarGraph(self, amps = 0, amps2 = 0, volts = 0, volts2 = 0))
        toggleGrid = wx.CheckBox(self, label="Show Grid")
        toggleGrid.Bind(wx.EVT_CHECKBOX, self.onToggleGrid)
        toggleLegend = wx.CheckBox(self, label="Show Legend")
        toggleLegend.Bind(wx.EVT_CHECKBOX, self.onToggleLegend)
 
        # layout the widgets
        mainSizer.Add(self.canvas, 1, wx.EXPAND)
        checkSizer.Add(toggleGrid, 0, wx.ALL, 5)
        checkSizer.Add(toggleLegend, 0, wx.ALL, 5)
        mainSizer.Add(checkSizer)
        self.SetSizer(mainSizer)


        
    #----------------------------------------------------------------------
    def onToggleGrid(self, event):
        """"""
        self.canvas.SetEnableGrid(event.IsChecked())
 
    #----------------------------------------------------------------------
    def onToggleLegend(self, event):
        """"""
        self.canvas.SetEnableLegend(event.IsChecked())

    def draw_graph(self, amps, amps2, volts, volts2):
        self.canvas.Draw(drawBarGraph(self, amps = amps, amps2 = amps2, volts = volts, volts2 = volts2))
            
def drawBarGraph(self, amps, amps2, volts, volts2):
    points1=[(amps,amps2), (volts,volts2)]
    line1 = PolyLine(points1, colour='green', legend='Feb.', width=10)

    return PlotGraphics([line1],
                        "Bar Graph - (Turn on Grid, Legend)", "Months", 
                        "Number of Students")
 