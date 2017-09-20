class DataObject(object):
    """Class used to compare values coming from serial and determine
     if they fall within the parameters specified by user input as well
      as calculate values such as power from incoming values"""
    
    Index = 0 # Used to keep track of how many objects have been created
    Vmax  = 20
    Vmin  = 10
    Amax  = 20
    Amin  = 10
    Tmax  = 100
    Tmin  = 10

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
    def checkerrorvoltage(self, volts):
        volt_ranges = ""
        if float(DataObject.Vmin) > float(volts) > float(DataObject.Vmax):
            print "error"
            volt_ranges = "error"
        else: 
            print "in range"
            volt_ranges = "in range"
    #Method to check if current falls within parameters
    def checkerrorcurrent(self, amps):
        amps_ranges = ""
        if float(DataObject.Amin) > float(amps) > float(DataObject.Amax):
            print "error"
            amps_ranges = "error"
        else: 
            print "in range"
            amps_ranges = "in range"