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

        #Set up regular expression
        self.time_re = re.compile(r'X(\d+):(\d+):(\d+),')
        self.frames_re = re.compile(r'frames=(\d+),')
    
    def connect(self,port):
        if not self.connected:
            self.port = port
            self.comm = serial.Serial(self.port,19200,timeout=0)
            self.comm.reset_input_buffer()
            self.connected = True
        
    def measure(self):
        '''
        Read in data from port and parse to measurements
        'X<minute>:<second>:<ms>,target=<ms>,frames=<number>,currentloops=<number>Z'
        '''
        dt = datetime.datetime.now()

        #Read in bytes from port
        dbytes = self.comm.in_waiting

        if dbytes > 0:
            rawdata = self.comm.read_until().decode('utf-8') 
            fails = {}

            #Parse measurements
            timeparse = re.findall(self.time_re,rawdata)
            framesparse = re.findall(self.frames_re,rawdata)

            if timeparse:
                self.data['sent_s'].append((dt,int(timeparse[0][1])))
                self.data['sent_ms'].append((dt,int(framesparse[0][2])))
            else:
                fails['sent_s'] = 'No data found'
                fails['sent_ms'] = 'No data found'

            if framesparse:
                self.data['frames'].append((dt,int(framesparse[0])))
            else:
                fails['frames'] = 'No data found'

            if fails:
                raise MeasureError(
                    self.name,
                    list(fails.keys()),
                    fails)




    