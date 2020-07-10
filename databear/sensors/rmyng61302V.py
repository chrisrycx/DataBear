'''
RM Young 61302V Barometric Pressure sensor
- DataBear Sensor Interface: V0.1
'''

import datetime
from databear.errors import MeasureError, SensorConfigError
import serial

class rmyoungBP:
    '''
    DataBear Sensor Interface V0.1
    '''
    def __init__(self,name,settings):
        '''
        Create a new Dyacon TPH sensor
        Inputs
        - name: string - name for sensor
        - settings: dictionary
            settings['serialnum'] = Serial Number 
            settings['measurement'] = Sensor measurement interval sec 
            settings['port'] = Serial port
            settings['baud'] = Baud rate
        '''
        try:
            self.name = name
            self.sn = settings['serialnumber']
            self.port = settings['port']
            self.frequency = settings['measurement']
            self.baud = settings['baud']
        except KeyError as ke:
            raise SensorConfigError('YAML missing required sensor setting')

        #Serial settings
        self.rs = 'RS232'
        self.duplex = 'full'
        self.resistors = 0
        self.bias = 0

        #Define characteristics of this sensor
        #Random guess at what might be a maximum sample frequency...
        self.maxfrequency = 5  #Maximum frequency in seconds the sensor can be polled
        self.timeout = 0.5

        #Set up connection
        self.comm = serial.Serial(self.port,self.baud,timeout=self.timeout)
        self.comm.reset_input_buffer()

        #Initialize data structure
        self.data = {'bp':[]}

    def measure(self):
        '''
        Read in data from RS232 serial port
        Data will have the form: dddd.dd
        '''
        dt = datetime.datetime.now()

        #Read in bytes from port
        dbytes = self.comm.in_waiting

        if dbytes > 0:
            rawdata = self.comm.read_until().decode('utf-8')
            bpnum = float(rawdata) 
            self.data['bp'].append((dt,bpnum))
            print('RMY - {}, value={}'.format(dt,bpnum))

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