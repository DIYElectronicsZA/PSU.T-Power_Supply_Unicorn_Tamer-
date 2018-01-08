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
    power = ""
    def __init__(self, volts, amps, temp, Vmax, Vmin, Amax, Amin, Tmax, Tmin, port=1):
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
        #Index = Index+1        
    
    def changeclassvariables(self):
        #TODO
        pass
    

    #Method to calculate power using voltage and amps coming from serial
    def calculatepower (self, volts, amps):
        timestr = time.strftime("Date: %Y-%m-%d Time: %H-%M-%S")
        DataObject.power = float(volts) * float(amps)
        DataObject.power = str(DataObject.power)
        fp = open('powervalue.txt', 'a')
        fp.write(str(DataObject.power))
        fp.write(' ')
        fp.write(timestr)
        fp.write('\n')
        fp.close()

    #Method to check if voltage falls within parameters
    def checkerrorvoltage(self, volts, volt_ranges, Vmax, Vmin):
        timestr = time.strftime("Date: %Y-%m-%d Time: %H-%M-%S")
        datestr = time.strftime("%Y-%m-%d")
        fname = str('Volts_Errors_' + str(datestr) + '.txt')
        f = open(fname, 'a')
        if float(Vmin) > float(volts):
            DataObject.volt_ranges = "Below range"
            DataObject.error_marker = DataObject.error_marker + 1
            f.write(volts)
            f.write(" Below range ")
            f.write(' ')
            f.write(timestr)
            f.write('\n')
        elif float(Vmax) < float(volts):
            DataObject.volt_ranges = "Above range"
            DataObject.error_marker = DataObject.error_marker + 1
            f.write(volts)
            f.write(" Above range ")
            f.write(' ')
            f.write(timestr)
            f.write('\n')
        else:
            DataObject.volt_ranges = "In range"
        f.close()

    #Method to check if current falls within parameters
    def checkerrorcurrent(self, amps, amps_ranges, Amax, Amin):
        timestr = time.strftime("Date: %Y-%m-%d Time: %H-%M-%S")
        datestr = time.strftime("%Y-%m-%d")
        fname = str('Current_Errors_' + str(datestr) + '.txt')
        f = open(fname, 'a')
        if float(Amin) > float(amps):
            DataObject.amps_ranges = "Below range"
            DataObject.error_marker = DataObject.error_marker + 1
            f.write(amps)
            f.write(" Below range ")
            f.write(timestr)
            f.write('\n')
        elif float(Amax) < float(amps):
            DataObject.amps_ranges = "Above range"
            DataObject.error_marker = DataObject.error_marker + 1
            f.write(amps)
            f.write(" Above range ")
            f.write(timestr)
            f.write('\n')
            print DataObject.error_marker
        else:
            DataObject.amps_ranges = "In range"
        f.close()
    
    def checkerrortemp(self,temp, temp_ranges, Tmax, Tmin):
        if float(Tmin) > float(temp):
            DataObject.temp_ranges = "Below range"
        elif float(Tmax) < float(temp):
            DataObject.temp_ranges = "Above range"
        else:
            DataObject.temp_ranges = "In range"
            
    def writetocsv(self, volts,amps,temp):
        with open('powersupply.csv', 'a') as csvfile:
            fieldnames = ['Port_number', 'Voltage', 'Current', 'Temperature']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            #writer.writeheader()   
            writer.writerow({'Port_number': '1', 'Voltage': volts, 'Current': amps, 'Temperature': temp})
            writer.writerow({'Port_number': '1', 'Voltage': volts, 'Current': amps, 'Temperature': temp})
       