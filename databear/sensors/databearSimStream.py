'''
A DataBear simulated streaming sensor
Utilizes simDataStream.py to generate data.

Expected incoming data format:
'X<minute>:<second>:<ms>,target=<ms>,frames=<number>,currentloops=<number>Z'
-- minute, second, and ms are the time when data is sent
-- target is the millisecond that data is scheduled to be sent
-- frames is the number of data frames sent
-- loops is the number of loops the simulator has performed

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
    measurements = ['sent_s','sent_ms','frames']
    measurement_description = {
        'sent_s':'seconds when data was sent',
        'sentms':'milliseconds when data was sent',
        'frames':'number of frames sent'
    } 
    units = {
        'sent_s':'s',
        'sent_ms':'ms',
        'frames':'count'
    }
    def __init__(self,name,sn,address,interval):
        '''
        Create a new sensor
        '''
        super().__init__(name,sn,address,interval)
       
        #Define characteristics of this sensor
        self.min_interval = 0
        self.connected = False
    
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
            rawdata = self.comm.read_until().decode('utf-8')

            #Parse measurements
            
            self.data['raw'].append((dt,rawdata))

    