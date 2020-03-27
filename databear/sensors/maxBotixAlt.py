'''
Maxbotix Altimeter
Initial sensor interface for Maxbotix Altimeter (model?)
- Tested platform(s): Dyacon MDL
- Interface Version: 0.1

'''

import datetime
import serial
import re

class maxbotixAlt:
    def __init__(self,name,settings):
        '''
        Inputs
            Inputs
            - Name for sensor
            - settings['serialnum'] = Serial Number
            - settings['port'] = Serial com port
            - settings['baud'] = Baud rate for sensor
        '''
        #Define characteristics of this sensor
        self.sensor_type = 'continuous'

        #Load sensor settings
        self.name = name
        self.sn = settings['serialnumber']
        self.port = settings['port']
        self.baud = settings['baud']
        self.timeout = 1
        self.maxfrequency = 0.1  #Maximum frequency in seconds the sensor can be polled
        
        #Serial settings
        self.rs = 'RS232'
        self.duplex = 'half'
        self.resistors = 0
        self.bias = 0

        #Set up connection
        self.comm = serial.Serial(self.port,self.baud,timeout=self.timeout)

        #Define measurements
        self.data = {'range':[]}
     
     
    def measure(self):
        '''
        Read in data from port and parse to measurements
        '''
        
        vals = None
        while not vals:
            dbytes = self.comm.in_waiting
            #print(dbytes)
            #rawdata = self.comm.read(dbytes).decode('utf-8')
            #rawdata = self.comm.readline().decode('utf-8') 
            ser = serial.Serial(self.port,self.baud,timeout=self.timeout)
            #rawdata = ReadLine.readline(ser)
            #rawdata = rl.readline()
            rawdata = self.comm.read_until(b'\r').decode('utf-8')
            
            #print('rawdata: {}'.format(rawdata))
            
            #Parse raw data
            #Pattern for decimal number
            #(see https://docs.python.org/3/library/re.html#writing-a-tokenizer)
            #dataRE = r'(\d+\.\d+)'
            dataRE = re.compile('\d\d\d\d')
            vals = re.findall(dataRE,rawdata) #Search for matches in rawdata
        vals = vals[0]
        dt = datetime.datetime.now()    
        timestamp = dt.strftime('%Y-%m-%d %H:%M:%S %f')
        #print('Measure: {}, data= {}'.format(timestamp,rawdata[:-2]))
        #print('vals = ')
        #print(vals)
        x = float(vals)
        
        self.data['range'].append((dt,x))

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

