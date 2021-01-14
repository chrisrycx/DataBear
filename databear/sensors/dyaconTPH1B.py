'''
Dyacon TPH-1B
This version is the older rev with no high resolution registers

'''

import minimalmodbus as mm
from databear.errors import MeasureError, SensorConfigError
from databear.sensors import sensor

class dyaconTPH1B(sensor.BusSensor):
    hardware_settings = {
        'serial':'RS485',
        'duplex':'half',
        'resistors':1,
        'bias':1
    }
    measurements = ['air_temperature','relative_humidity','barometric_pressure']
    units = {
        'air_temperature':'C',
        'relative_humidity':'%',
        'barometric_pressure':'mb'
    }
    min_interval = 1  #Minimum interval that sensor can be polled
    uses_portlock = True
    registers = {
            'air_temperature':201,
            'relative_humidity':202,
            'barometric_pressure':203
        }
    def connect(self,port,portlock):
        self.portlock=portlock
        if not self.connected:
            self.port = port
            self.comm = mm.Instrument(self.port,self.address)
            self.comm.serial.timeout = 0.3
            self.connected = True

    def readMeasure(self,starttime):
        '''
        Read in data using modbus
        '''
        fails = {} #keep track of measurement failures
        for measure in self.measurements:
            
            try:
                val = self.comm.read_register(self.registers[measure],signed=True)
                val = val/10

                self.data[measure].append((starttime,val))
                
            except mm.NoResponseError as norsp:
                fails[measure] = 'No response from sensor'
            except:
                raise 
        
        #Raise a measurement error if a fail is detected
        if len(fails)>0:
            failnames = list(fails.keys())
            raise MeasureError(self.name,failnames,fails)
    
   
   


  
