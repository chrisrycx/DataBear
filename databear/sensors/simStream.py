'''
Simulated streaming sensor
- Platform: Windows
- Connection: USB-RS485 (loopback)
- Interface: DataBear Sensor Interface V0
'''

import datetime
import serial
import re

class StreamSensor:
    def __init__(self,name,settings):
        '''
        Abstract class for a streaming sensor
        Inputs
            - settings['serialnumber']
            - settings['port']
            - settings['baud']
            - settings['hz'] - Data stream frequency from sensor
        '''
        #Define characteristics of this sensor
        self.sensor_type = 'continuous'

        #Load sensor settings
        self.name = name
        self.sn = settings['serialnumber']
        self.port = settings['port']
        self.baud = settings['baud']
        self.timeout = 0

        #Serial settings
        self.rs = 'RS485'
        self.duplex = 'half'
        self.resistors = 1
        self.bias = 1

        #Set up connection
        self.comm = serial.Serial(self.port,self.baud,timeout=self.timeout)

        #Define measurements
        self.data = {'x':[],'y':[],'z':[]}
        
    def measure(self):
        '''
        Read in data from port and parse to measurements
        '''
        dt = datetime.datetime.now()

        dbytes = self.comm.in_waiting
        rawdata = self.comm.read(dbytes).decode('utf-8')
        timestamp = dt.strftime('%Y-%m-%d %H:%M:%S %f')
        print('Measure: {}, data= {}'.format(timestamp,rawdata[:-2]))

        '''
        #Parse raw data
        #Pattern for decimal number
        #(see https://docs.python.org/3/library/re.html#writing-a-tokenizer)
        dataRE = r'(\d+\.\d+)'
        vals = re.findall(dataRE,rawdata) #Search for matches in rawdata

        x = float(vals[0])
        y = float(vals[1])
        z = float(vals[2])

        self.data['x'].append((dt,x))
        self.data['y'].append((dt,y))
        self.data['z'].append((dt,z))
        '''

    def cleardata(self,name):
        '''
        Clear data values for a particular measurement
        '''
        self.data[name] = []
