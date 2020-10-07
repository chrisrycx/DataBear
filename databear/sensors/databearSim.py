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
    measurements = ['second1','second2','counter']
    measurement_description = {
        'second1':'The second from the current datetime',
        'second2':'Same as second1, used for comparison',
        'counter':'The count of the number of measurements'
    } 
    units = {
        'second1':'s',
        'second2':'s',
        'counter':'count'
    }
    def __init__(self,name,sn,address):
        '''
        Create a new simulator
        - Call base class init
        - Override base data structure
        '''
        super().__init__(name,sn,address)

        #Initialize a counter
        self.counter = 0 

    def measure(self):
        '''
        Override base method
        - Load simulated measurements
        '''
        #Create a timestamp
        dt = datetime.datetime.now()
        self.counter = self.counter + 1

        #Randomly raise measurement error for testing
        if random.randint(0,5) == 3:
            raise MeasureError(self.name,['second1'],{'second1':'Test failure'})

        #Measurements are simply integers from the dt
        self.data['second1'].append((dt,dt.second))
        self.data['second2'].append((dt,dt.second))
        self.data['counter'].append((dt,self.counter))

        #Pause to simulate a measurement time
        time.sleep(0.5)

