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
    measurements = ['seconds']
    measurement_description = {
        'seconds':'Seconds associated with timestamp',
    } 
    units = {
        'seconds':'s'
    }
    min_interval = 2

    def measure(self):
        '''
        Override base method
        - Load simulated measurements
        '''
        #Create a timestamp
        dt = datetime.datetime.now()

        #Measurements are simply integers from the dt
        self.data['seconds'].append((dt,dt.second))

        #Pause to simulate a measurement time
        time.sleep(1.5)

