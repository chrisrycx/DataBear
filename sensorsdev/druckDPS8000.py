'''
GE Druck DPS 8000 pressure sensor
- DataBear Sensor Interface V0.1

** Assumes "direct" mode of comm, addressing not yet implemented
'''

import datetime
import serial
import time
from databear.errors import MeasureError, SensorConfigError

class dps8000:
    interface_version = '0.1'
    def __init__(self,name,settings):
        '''
        Create a new Dyacon TPH sensor
        Inputs
            - Name for sensor
            - settings['serialnum'] = Serial Number
            - settings['port'] = Serial com port
            - settings['address'] = Sensor modbus address
            - settings['baud'] = Baud rate
        '''
        try:
            self.name = name
            self.sn = settings['serialnumber']
            self.port = settings['port']
            self.address = settings['address']
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
        self.maxfrequency = 1  #Maximum frequency in seconds the sensor can be polled

        #Set up connection
        self.timeout = 1
        self.comm = serial.Serial(self.port,self.baud,timeout=self.timeout)
        self.comm.reset_input_buffer()

        #Initialize data structure
        self.data = {'pressure':[]} #Empty data dictionary

    def measure(self):
        '''
        Read in data from the sensor
        '''
        failnames = ['pressure']
        fails = {}
        try:
            dt = datetime.datetime.now()

            #Send a request for measurement
            cmd = 'R\r'
            self.comm.write(cmd.encode('utf-8'))

            #Wait for response
            time.sleep(0.5)
            response = self.comm.read(size=10)

            #Parse response - should just be a number
            pressure = float(response)

        except serial.SerialTimeoutException as norsp:
            fails['pressure'] = 'No response from sensor'
            raise MeasureError(self.name,failnames,fails)
        except ValueError as ve:
            fails['pressure'] = 'Cannot convert data to float'
            raise MeasureError(self.name,failnames,fails)

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
