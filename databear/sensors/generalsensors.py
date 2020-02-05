'''

General Sensor classes
- ** use as base classes someday??

'''

from databear.sensors import sensorfactory
import datetime
import serial

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
        x = {'name':'x','dataRE':'test'}
        y = {'name':'y','dataRE':'test'}
        z = {'name':'z','dataRE':'test'}
        self.measurements = [x,y,z]

        #Initialize data structure
        self.data = {} #Empty data dictionary

    def measure(self):
        '''
        Read in data from port and parse to measurements
        '''
        dt = datetime.datetime.now()

        dbytes = self.comm.in_waiting
        rawdata = self.comm.read(dbytes).decode('utf-8')
        print(rawdata)

        for measure in self.measurements:
            #Parse measurement data from raw data
            data = (dt,55)
            self.data[measure['name']] = [data] #***Testing


    def cleardata(self,name):
        '''
        Clear data values for a particular measurement
        '''
        self.data[name] = []

#Register sensor with factory
sensorfactory.factory.register_sensor('streaming',StreamSensor)