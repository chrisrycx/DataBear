'''
A Template for building a sensor class.
Change and add content following comments.

General Information Regarding This Class
- Platform: Any
- Connection: Any
- Interface: DataBear Sensor Interface V0.1
'''

#Import any libraries needed for sensor operation. Also
#import error classes to alert users to problems.
import datetime
from databear.errors import MeasureError, SensorConfigError

#Recommended class name: <manufacturer><sensor model> ie. dyaconTPH1
class databearTemplate:
    '''
    Define a sensor class following DataBear
    sensor class interface.
    Recommended class name: 
    <manufacturer><sensor model> ie. dyaconTPH1
    '''
    def __init__(self,name,settings):
        '''
        Create a new sensor
        Inputs
        - name: string - name for sensor
        - settings: dictionary
            settings['serialnum'] = Serial Number (required)
            settings['frequency'] = Sensor measurement frequency in sec (required)
            settings[<other>] = Any other user configurable setting
        '''
        #Load settings to instance attributes
        try:
            self.name = name
            self.sn = settings['serialnumber']
            self.frequency = settings['frequency']
            #Add other variables as necessary
        except KeyError as ke:
            raise SensorConfigError('YAML missing required sensor setting')

        #Define non-user configurable sensor settings
        self.maxfrequency = 1  #Required: Maximum frequency in seconds the sensor can be polled

        #Initialize data structure
        #Dictionary of the form {<measurement>:[],...}
        #This will determine the name(s) of each measurement made by the sensor
        self.data = {'measure1':[],'measure2':[],'measure3':[]}

    def measure(self):
        '''
        1. Aquire data from sensor for all measurements.
           All data must be given a timestamp.
        2. Add data to self.data
           self.data['measure1'].append((dt,val))
           dt is a datetime
           val is the value of the measurement

        Code should raise a MeasureError when
        there is a problem.
        '''
        pass

    def getdata(self,name,startdt,enddt):
        '''
        Return a list of values such that
        startdt <= timestamps < enddt
        - Inputs: datetime objects
        '''
        output = []
        data = self.data[name]
        for val in data:
            if (val[0]>=startdt) and (val[0]<enddt):
                output.append(val)
        return output


    def cleardata(self,name,startdt,enddt):
        '''
        Clear data values for a particular measurement
        Loop through values and remove. Note: This is probably
        inefficient if the data structure is large.
        '''
        savedata = []
        data = self.data[name]
        for val in data:
            if (val[0]<startdt) or (val[0]>=enddt):
                savedata.append(val)

        self.data[name] = savedata
