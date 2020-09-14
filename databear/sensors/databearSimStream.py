'''
A DataBear simulated streaming sensor
Utilizes simDataStream.py to generate data.

Setup:
- Windows: loopback USB-RS485 and run both simDataStream and DataBear
- Other: Connect PC to device and run simDataStream

'''

import datetime
from databear.errors import MeasureError, SensorConfigError
from databear.sensors import sensor
import serial
import re

class databearSimStream(sensor.Sensor):
    hardware_settings = {
        'serial':'RS485',
        'duplex':'half',
        'resistors':1,
        'bias':1
    }
    def __init__(self,name,sn,address,interval):
        '''
        Create a new sensor
        '''
        super().__init__(name,sn,address,interval)
       
        
        #Define characteristics of this sensor
        self.min_interval = 0
        self.connected = False

        #Initialize data structure
        self.data = {'raw':[]}
    
    def connect(self,port):
        if not self.connected:
            self.port = port
            self.comm = serial.Serial(self.port,19200,timeout=0)
            self.comm.reset_input_buffer()
            self.connected = True
        
    def measure(self):
        '''
        Read in data from port and parse to measurements
        '''
        dt = datetime.datetime.now()

        #Read in bytes from port
        dbytes = self.comm.in_waiting

        if dbytes > 0:
            rawdata = self.comm.read(dbytes).decode('utf-8')
            self.data['raw'].append((dt,rawdata))

    