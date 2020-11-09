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
    measurements = ['sentdiff','targetdiff']
    measurement_description = {
        'sentdiff':'millisecond difference between send and receive',
        'targetdiff':'millisecond difference between schedule and send',
    } 
    units = {
        'sentdiff':'ms',
        'targetdiff':'ms'
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
        self.frames_re = re.compile(r'targetdiffms=(\d+),')
    
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
            fails = {}

            #Parse measurements
            timeparse = re.findall(self.time_re,rawdata)
            targetparse = re.findall(self.frames_re,rawdata)

            if timeparse:
                #Extract time sent
                sent_m = int(timeparse[0][0])
                sent_s = int(timeparse[0][1])
                sent_mcs = int(timeparse[0][2])

                #Convert to datetime
                sent_dt = datetime.datetime(
                    dt.year,
                    dt.month,
                    dt.day,
                    dt.hour,
                    sent_m,
                    sent_s,
                    sent_mcs
                )

                delay_ms = int((dt - sent_dt)/datetime.timedelta(milliseconds=1))
                self.data['sentdiff'].append((dt,delay_ms))
            else:
                fails['sentdiff'] = 'No data found'

            if targetparse:
                self.data['targetdiff'].append((dt,int(targetparse[0])))
            else:
                fails['targetdiff'] = 'No data found'

            if fails:
                raise MeasureError(
                    self.name,
                    list(fails.keys()),
                    fails)




    