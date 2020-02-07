'''

General Sensor classes
- ** use as base classes someday??

'''

from databear.sensors import sensorfactory
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

        #Set up connection
        self.comm = serial.Serial(self.port,self.baud,timeout=self.timeout)

        #Define measurements
        x = {'name':'x'}
        y = {'name':'y'}
        z = {'name':'z'}
        self.measurements = [x,y,z]

        #Initialize data structure
        self.data = {'x':[],'y':[],'z':[]} #Empty data dictionary

    def measure(self):
        '''
        Read in data from port and parse to measurements
        '''
        dt = datetime.datetime.now()

        dbytes = self.comm.in_waiting
        rawdata = self.comm.read(dbytes).decode('utf-8')
        print(rawdata)

        #Parse raw data
        dataRE = r'(\d+\.\d+)'  #Pattern for decimal number (see https://docs.python.org/3/library/re.html#writing-a-tokenizer)
        m = re.findall(dataRE,rawdata) #Search for matches in rawdata

        counter=0
        for measure in self.measurements:
            #Parse measurement data from raw data
            val = float(m[counter])
            data = (dt,val)
            self.data[measure['name']].append(data)
            counter=counter+1


    def cleardata(self,name):
        '''
        Clear data values for a particular measurement
        '''
        self.data[name] = []

#Register sensor with factory
sensorfactory.factory.register_sensor('streaming',StreamSensor)