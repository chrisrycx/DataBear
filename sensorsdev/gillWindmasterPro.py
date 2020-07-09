'''
Gill Windmaster Pro Sensor
Interface: V0.1
'''

import datetime
import serial
import re
import pdb

class gillWindmasterPro:
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
        self.sensortype = 'stream'  # this doesn't do anything right now? May be redundant with what is specified in yaml. Where is best spot?

        #Load sensor settings
        self.name = name
        self.sn = settings['serialnumber']
        self.port = settings['port']
        self.baud = settings['baud']
        self.timeout = 1
        self.maxfrequency = 0.03  #Maximum frequency in seconds the sensor can be polled, 32 Hz
        self.nBytes = 53   # ****** number of bytes in line of data, seems to be the only way to deal with fast data rates

        
        #Serial settings
        self.rs = 'RS232'
        self.duplex = 'half'
        self.resistors = 0
        self.bias = 0
        
        #Set up connection
        self.comm = serial.Serial(self.port,self.baud,timeout=self.timeout)

        #Define measurements
        self.data = {'gillWindmasterPro':[]}
        self.dataRE = re.compile('[A-Z],[+-]\d+.\d+,[+-]\d+.\d+,[+-]\d+.\d+,[A-Z],[+-]\d+.\d+,[+-]\d+.\d+,\S+,\S+')   # note there is ascii vs unicode matching, if having trouble look into
        self.lastLength = None
         
     
    def measure(self):
        '''
        Read in data from port and parse to measurements
        '''
        
        vals = None
        rawdata = str()
        while not vals:
            # if last rawdata value wasn't right length, go bit by bit until end of line then start reading by nBytes
            if self.lastLength != self.nBytes:
                print('finding end of line of data')
                self.comm.flushInput()  # flush input buffer so getting current data
                while True:
                    oneByte = self.comm.read(1)
                    if oneByte == b"\n":
                        break
                print('Got it collecting data')
            dt = datetime.datetime.now()    
            timestamp = dt.strftime('%Y-%m-%d %H:%M:%S %f')
            raw = self.comm.read(self.nBytes)
            rawdata = rawdata+raw.decode('utf-8')
            self.lastLength = len(rawdata)
            
            
            #Parse raw data
            vals = re.findall(self.dataRE,rawdata) #Search for matches in rawdata
        
        vals = re.split(',',vals[0])
        dt = datetime.datetime.now()    
        timestamp = dt.strftime('%Y-%m-%d %H:%M:%S %f')
        vals.insert(0,timestamp)
        self.data['gillWindmasterPro'].append((dt,vals))
        
    def getdata(self,name,startdt,enddt):
            '''
            Return a list of values such that
            startdt <= timestamps < enddt
            - Inputs: datetime objects
            '''
            output = []
            data = self.data[name]
            
            for val in data:
                #if (val[0]>=startdt) and (val[0]<enddt):    # is this why its not always writing data
                output.append(val)
            return output
        
    def cleardata(self,name):
        '''
        Clear data values for a particular measurement
        '''
        self.data[name] = []