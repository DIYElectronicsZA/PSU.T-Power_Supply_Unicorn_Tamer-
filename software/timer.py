import random
import wx
import serial

class Frame(wx.Frame):

      

    
    def __init__(self):
        super(Frame, self).__init__(None)
        self.SetTitle('Title')
        panel = wx.Panel(self)
        style = wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE
        self.text = wx.StaticText(panel, style=style)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer(1)
        sizer.Add(self.text, 0, wx.EXPAND)
        sizer.AddStretchSpacer(1)
        panel.SetSizer(sizer)
        self.on_timer()
    def on_timer(self):
        countdown = 30
        ser= serial.Serial('COM7', 115200)
        while countdown > 0:
            value_PSU = ser.readline()
            countdown = countdown -1
            nwstuff = value_PSU.split(',')
        self.text.SetLabel(str(nwstuff[1]))
        wx.CallLater(100, self.on_timer)

if __name__ == '__main__':
    app = wx.App()
    frame = Frame()
    frame.Show()
    app.MainLoop()