'''
A sensor simulator for use in testing
Creates simple data values when measure method is called
'''

import datetime
import time
import random #To simulate a failure to communicate
from databear.errors import MeasureError, SensorConfigError
from databear.sensors import sensor

class databearSim(sensor.Sensor):
    def __init__(self,name,sn,address,interval):
        '''
        Create a new simulator
        - Call base class init
        - Override base data structure
        '''
        super().__init__(name,sn,address,interval)

        #Initialize data structure
        self.counter = 0 #measure 3 will simply be a measurement count
        self.data = {'second':[],'second2':[],'counter':[]}

    def measure(self):
        '''
        Override base method
        - Load simulated measurements
        '''
        #Create a timestamp
        dt = datetime.datetime.now()
        self.counter = self.counter + 1

        #Randomly raise measurement error in measurement 1 for testing
        if random.randint(0,5) == 3:
            raise MeasureError(self.name,['measure1'],{'measure1':'Test failure'})

        #Measurements are simply integers from the dt
        self.data['simsecond'].append((dt,dt.second))
        self.data['simsecond2'].append((dt,dt.second))
        self.data['counter'].append((dt,self.counter))

        #Pause to simulate a measurement time
        time.sleep(0.5)

