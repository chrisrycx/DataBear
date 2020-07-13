'''
A sensor simulator for use in testing

Creates simple data values when measure method is called
Sensor Interface: V0.1
'''
import datetime
import time
from databear.errors import MeasureError, SensorConfigError
import random

class sensorSim:
    '''
    Define a sensor class following DataBear
    sensor class interface.
    Recommended class name: 
    <manufacturer><sensor model> ie. dyaconTPH1
    '''
    interface_version = '0.1'
    def __init__(self,name,settings):
        '''
        Create a new sensor
        Inputs
        - name: string - name for sensor
        - settings: dictionary
            settings['serialnum'] = Serial Number (required)
            settings['measurement'] = Sensor measurement frequency in sec (required)
            settings[<other>] = Any other user configurable setting
        '''
        #Load settings to instance attributes
        try:
            self.name = name
            self.sn = settings['serialnumber']
            self.frequency = settings['measurement']
            #Add other variables as necessary
        except KeyError as ke:
            raise SensorConfigError('YAML missing required sensor setting')

        #Define non-user configurable sensor settings
        self.port = None
        self.maxfrequency = 1  #Required: Maximum frequency in seconds the sensor can be polled

        #Initialize data structure
        #Dictionary of the form {<measurement>:[],...}
        #This will determine the name(s) of each measurement made by the sensor
        self.counter = 0 #measure 3 will simply be a measurement count
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
        #Create a timestamp
        dt = datetime.datetime.now()
        self.counter = self.counter + 1

        #Randomly raise measurement error in measurement 1 for testing
        if random.randint(0,5) == 3:
            raise MeasureError(self.name,['measure1'],{'measure1':'Test failure'})

        #Measurements are simply integers from the dt
        self.data['measure1'].append((dt,dt.second))
        self.data['measure2'].append((dt,dt.second))
        self.data['measure3'].append((dt,self.counter))

        #Print for testing
        print('{}  Time: {}  measures 1 and 2: {}  measure3: {}'.format(
            self.name,dt.strftime('%M:%S:%f'),dt.second,self.counter
        ))

        #Pause to simulate a measurement time
        time.sleep(0.5)

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
