'''
A DataBear simulated streaming sensor
Utilizes simDataStream.py to generate data.

Expected incoming data format:
'X<minute>:<second>:<ms>,targetdiffms=<ms>Z'
-- minute, second, and ms are the time when data is sent
-- targetdiffms is the millisecond diff between schedule and send

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
    measurements = ['sendtime']
    measurement_description = {
        'sendtime':'local clock seconds when data was sent',
    } 
    units = {
        'sendtime':'s',
    }
    def __init__(self,name,sn,address):
        '''
        Create a new sensor
        '''
        super().__init__(name,sn,address)

        #Set up regular expression
        self.time_re = re.compile(r'=(\d+.\d+)Z')
    
    def connect(self,port):
        if not self.connected:
            self.port = port
            self.comm = serial.Serial(self.port,19200,timeout=0.5)
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
            fails = {}

            #Parse measurements
            timeparse = re.findall(self.time_re,rawdata)

            if timeparse:
                #Extract time sent
                sendtime = float(timeparse[0])
                self.data['sendtime'].append((dt,sendtime))
            else:
                fails['sendtime'] = 'No data found'

            if fails:
                raise MeasureError(
                    self.name,
                    list(fails.keys()),
                    fails)
        




    