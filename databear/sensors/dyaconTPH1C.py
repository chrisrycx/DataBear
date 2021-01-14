'''
Dyacon TPH-1C Sensor
This is the newer version with high resolution registers

'''

import datetime
import minimalmodbus as mm
from databear.errors import MeasureError, SensorConfigError
from databear.sensors import sensor

class dyaconTPH1C(sensor.BusSensor):
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
        'air_temperature':210,
        'relative_humidity':212,
        'barometric_pressure':214
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
            dt = datetime.datetime.now()
            
            try:
                val = self.comm.read_float(self.registers[measure])
                self.data[measure].append((starttime,val))

            except mm.NoResponseError as norsp:
                fails[measure] = 'No response from sensor'

            except:
                raise
                
        #Raise a measurement error if a fail is detected
        if len(fails)>0:
            failnames = list(fails.keys())
            raise MeasureError(self.name,failnames,fails)
    
    
