class DataObject(object):
    """Class used to compare values coming from serial and determine
     if they fall within the parameters specified by user input as well
      as calculate values such as power from incoming values"""
    
    Index = 0 # Used to keep track of how many objects have been created
    Vmax  = 15
    Vmin  = 10
    Amax  = 15
    Amin  = 10
    Tmax  = 100
    Tmin  = 10
    volt_ranges = "nothing"
    amps_ranges = "nothing"
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
        power = float(volts) * float(amps)
        print power

    #Method to check if voltage falls within parameters
    def checkerrorvoltage(self, volts, volt_ranges):
        if float(DataObject.Vmin) > float(volts):
            DataObject.volt_ranges = "Below range"
        elif float(DataObject.Vmax) < float(volts):
            DataObject.volt_ranges = "Above range"
        else:
            DataObject.volt_ranges = "In range"

    #Method to check if current falls within parameters
    def checkerrorcurrent(self, amps, amps_ranges):
        if float(DataObject.Amin) > float(amps):
            DataObject.amps_ranges = "Below range"
        elif float(DataObject.Amax) < float(amps):
            DataObject.amps_ranges = "Above range"
        else:
            DataObject.amps_ranges = "In range"