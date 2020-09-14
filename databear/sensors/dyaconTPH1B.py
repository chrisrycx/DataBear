'''
Dyacon TPH-1B
This version is the older rev with no high resolution registers

'''

import datetime
import minimalmodbus as mm
from databear.errors import MeasureError, SensorConfigError
from databear.sensors import sensor

class dyaconTPH(sensor.Sensor):
    hardware_settings = {
        'serial':'RS485',
        'duplex':'half',
        'resistors':1,
        'bias':1
    }
    def __init__(self,name,sn,address,interval):
        '''
        Override base class
        '''
        super().__init__(name,sn,address,interval)

        #Define characteristics of this sensor
        self.min_interval = 1  #Minimum interval that sensor can be polled

        #Define measurements
        airT = {'name':'airT','register':201}
        rh = {'name':'rh','register':202}
        bp = {'name':'bp','register':203}
        self.measurements = [airT,rh,bp]

        #Initialize data structure
        self.data = {'airT':[],'rh':[],'bp':[]} #Empty data dictionary
        self.connected = False

    def connect(self,port):
        if not self.connected:
            self.port = port
            self.comm = mm.Instrument(self.port,self.address)
            self.comm.serial.timeout = 0.3
            self.connected = True

    def measure(self):
        '''
        Read in data using modbus
        '''
        fails = {} #keep track of measurement failures
        for measure in self.measurements:
            dt = datetime.datetime.now()
            timestamp = dt.strftime('%Y-%m-%d %H:%M:%S %f')
            
            try:
                val = self.comm.read_register(measure['register'],signed=True)
                val = val/10

                #Output results for testing
                print('{} - Measure {}: {}, value= {}'.format(
                    self.name,
                    measure['name'],
                    timestamp,
                    val))

                self.data[measure['name']].append((dt,val))
            except mm.NoResponseError as norsp:
                fails[measure['name']] = 'No response from sensor'
        #Raise a measurement error if a fail is detected
        if len(fails)>0:
            failnames = list(fails.keys())
            raise MeasureError(self.name,failnames,fails)
    
   
   


  
