'''
Dyacon DataStream
A testing module for reading streaming data from simDataStream.py 
- Platform: Windows, Linux
- Tested hardware: USB-RS485 (loopback)
- Interface: DataBear Sensor Interface V0.1
'''
#Import any libraries needed for sensor operation. Also
#import error classes to alert users to problems.
import datetime
from databear.errors import MeasureError, SensorConfigError
import serial
import re

class dyaconDataStream:
    def __init__(self,name,settings):
        '''
        Create a new sensor
        Inputs
        - name: string - name for sensor
        - settings: dictionary
            settings['serialnum'] = Serial Number 
            settings['measurement'] = Sensor measurement interval sec 
            settings['port'] = Serial port
            settings['baud'] = Baud rate
        '''
        #Load settings to instance attributes
        try:
            self.name = name
            self.sn = settings['serialnumber']
            self.frequency = settings['measurement']
            self.port = settings['port']
            self.baud = settings['baud']
            
        except KeyError as ke:
            raise SensorConfigError('YAML missing required sensor setting')
        
        #Other settings
        self.maxfrequency = 0  #Maximum sample rate
        self.timeout = 0

        #Set up connection
        self.comm = serial.Serial(self.port,self.baud,timeout=self.timeout)

        #Initialize data structure
        #See simDataStream.py
        #micsecdiff = send microseconds - target microseconds
        #Frame is the number of frames sent in a particular second
        #Loops is the number of loops between frames on simDataStream
        self.data = {'micsecdiff':[],'frames':[],'loops':[]}
        
    def measure(self):
        '''
        Read in data from port and parse to measurements
        '''
        dt = datetime.datetime.now()

        #Read in bytes from port
        dbytes = self.comm.in_waiting
        rawdata = self.comm.read(dbytes).decode('utf-8')

        if dbytes > 0:
            #Parse data
            #Expects: 'X{}:{}:{},target={},frames={},currentloops={}\r\n'
            framere = r'X\d+:\d+:(\d+),target=(\d+),frames=(\d+),currentloops=(\d+)\r\n'
            frameparse = re.findall(framere,rawdata)
            framematch = frameparse[0] #Assumes only one match in raw data
            mcdiff = int(framematch[0]) - int(framematch[1])
            self.data['micsecdiff'].append((dt,mcdiff))
            self.data['frames'].append((dt,framematch[2]))
            self.data['loops'].append((dt,framematch[3]))

    def getdata(self,name,startdt,enddt):
            '''
            Return a list of values such that
            startdt <= timestamps < enddt
            - Inputs: datetime objects
            '''
            output = []
            data = self.data[name]
            for val in data:
                if (val[0]>=startdt) and (val[0]<enddt):
                    output.append(val)
            return output
        
    def cleardata(self,name,startdt,enddt):
        '''
        Clear data values for a particular measurement
        Loop through values and remove. Note: This is probably
        inefficient if the data structure is large.
        '''
        savedata = []
        data = self.data[name]
        for val in data:
            if (val[0]<startdt) or (val[0]>=enddt):
                savedata.append(val)

        self.data[name] = savedata
