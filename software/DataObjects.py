class DataObject(object):
    """Class used to compare values coming from serial and determine
     if they fall within the parameters specified by user input as well
      as calculate values such as power from incoming values"""
    
    Index = 0 # Used to keep track of how many objects have been created
    Vmax  = 13
    Vmin  = 11
    Amax  = 12
    Amin  = 8
    Tmax  = 40
    Tmin  = 10
    volt_ranges = "nothing"
    amps_ranges = "nothing"
    temp_ranges = "nothing"
    power = ""
    def __init__(self,volts, amps, temp, port=1):
        """Class constructor"""
        self.Volt = volts
        self.Amps = amps
        self.Temp = temp
        self.Port = port
        #Index = Index+1 
        
    
    def changeclassvariables(self):
        #TODO
        pass
    

    #Method to calculate power using voltage and amps coming from serial
    def calculatepower (self, volts, amps):
        DataObject.power = float(volts) * float(amps)
        DataObject.power = str(DataObject.power)
        fp = open('powervalue.txt', 'a')
        fp.write(str(DataObject.power))
        fp.write('\n')
        fp.close()

    #Method to check if voltage falls within parameters
    def checkerrorvoltage(self, volts, volt_ranges):
        f = open('voltsvalue.txt', 'a')
        if float(DataObject.Vmin) > float(volts):
            DataObject.volt_ranges = "Below range"
            f.write(volts)
            f.write("Below range")
            f.write('\n')
        elif float(DataObject.Vmax) < float(volts):
            DataObject.volt_ranges = "Above range"
            f.write(volts)
            f.write("Above range")
            f.write('\n')
        else:
            DataObject.volt_ranges = "In range"
        f.close()

    #Method to check if current falls within parameters
    def checkerrorcurrent(self, amps, amps_ranges):
        f = open('ampssvalue.txt', 'a')
        if float(DataObject.Amin) > float(amps):
            DataObject.amps_ranges = "Below range"
            f.write(amps)
            f.write("Below range")
            f.write('\n')
        elif float(DataObject.Amax) < float(amps):
            DataObject.amps_ranges = "Above range"
            f.write(amps)
            f.write("Above range")
            f.write('\n')
        else:
            DataObject.amps_ranges = "In range"
        f.close()
    
    def checkerrottemp(self,temp):
        if float(DataObject.Tmin) > float(temp):
            DataObject.temp_ranges = "Below range"
        elif float(DataObject.Tmax) < float(temp):
            DataObject.temp_ranges = "Above range"
        else:
            DataObject.temp_ranges = "In range"           
            