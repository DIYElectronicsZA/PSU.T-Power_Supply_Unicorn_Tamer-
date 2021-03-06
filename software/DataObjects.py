import time
import csv

class DataObject(object):
    """Class used to compare values coming from serial and determine
     if they fall within the parameters specified by user input as well
      as calculate values such as power from incoming values"""   
    Index = 0 # Used to keep track of how many objects have been created
   # Vmax  = 0
   # Vmin  = 0
   # Amax  = 0
   # Amin  = 0
   # Tmax  = 0
   # Tmin  = 0
    error_marker = 0
    volt_ranges = "nothing"
    amps_ranges = "nothing"
    temp_ranges = "nothing"
    power_ranges = "Watts"
    power = ""
    volts_list = []
    amps_list = []

    def __init__(self, volts, amps, temp, Vmax, Vmin, Amax, Amin, Tmax, Tmin, port):
        """Class constructor"""
        
        self.Volt = volts
        self.Amps = amps
        self.Temp = temp
        self.Port = port
        self.Vmax  = Vmax
        self.Vmin  = Vmin
        self.Amax  = Amax
        self.Amin  = Amin
        self.Tmax  = Tmax
        self.Tmin  = Tmin
        self.port = port
 
        #self.graph_panel = panel_one.draw_graph(self,amps= 0, amps2= 0, volts = 0, volts2 = 0)
        #Index = Index+1        
    
    def changeclassvariables(self):
        #TODO
        pass
    

    #Method to calculate power using voltage and amps coming from serial
    def calculatepower (self, volts, amps):
        timestr = time.strftime("Date: %Y-%m-%d Time: %H-%M-%S")
        try:
            DataObject.power = float(volts) * float(amps)
            DataObject.power = str(DataObject.power)
            return DataObject.power
        except:
            pass
            
    #Method to check if voltage falls within parameters
    def checkerrorvoltage(self, volts, volt_ranges, Vmax, Vmin):
        timestr = time.strftime("Date: %Y-%m-%d Time: %H-%M-%S")
        datestr = time.strftime("%Y-%m-%d")
        #print DataObject.serial_port.error_on
        #while DataObject.serial_port.error_on > 0:
        if float(Vmin) > float(volts):
            DataObject.volt_ranges = "Below range"
            DataObject.error_marker = DataObject.error_marker + 1
        elif float(Vmax) < float(volts):
            DataObject.volt_ranges = "Above range"
            DataObject.power_ranges = "Above range"
            DataObject.error_marker = DataObject.error_marker + 1
        else:
            DataObject.volt_ranges = "In range"

    #Method to check if current falls within parameters
    def checkerrorcurrent(self, amps, amps_ranges, Amax, Amin, offset):
        timestr = time.strftime("Date: %Y-%m-%d Time: %H-%M-%S")
        datestr = time.strftime("%Y-%m-%d")
        #while DataObject.serial_port.error_on > 0:
        amps = (float(amps) - float(offset))
        if float(Amin) > float(amps):
            DataObject.amps_ranges = "Below range"
            DataObject.error_marker = DataObject.error_marker + 1
        elif float(Amax) < float(amps):
            DataObject.amps_ranges = "Above range"
            DataObject.error_marker = DataObject.error_marker + 1
        else:
            DataObject.amps_ranges = "In range"
    
    def checkerrortemp(self,temp, temp_ranges, Tmax, Tmin):
        if float(Tmin) > float(temp):
            DataObject.temp_ranges = "Below range"
            DataObject.error_marker = DataObject.error_marker + 1
        elif float(Tmax) < float(temp):
            DataObject.temp_ranges = "Above range"
            DataObject.error_marker = DataObject.error_marker + 1
        else:
            DataObject.temp_ranges = "In range"
            

   
    def make_list(self,amps,volts):

        DataObject.volts_list.append(volts)
        DataObject.amps_list.append(amps)
        

