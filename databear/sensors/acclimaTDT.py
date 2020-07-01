'''
Acclima TDT SDI-12 Sensor
- DataBear Sensor Interface: V0.1

** Initial development with limited functionality

'''

import datetime
from databear.errors import MeasureError, SensorConfigError

#Imports for SDI12 sensors
import serial
import time

class acclimaTDT:
    '''
    DataBear Sensor Interface V0.1
    '''
    def __init__(self,name,settings):
        '''
        Create a new Dyacon TPH sensor
        Inputs
            - Name for sensor
            - settings['serialnum'] = Serial Number
            - settings['port'] = Serial com port
            - settings['address'] = Sensor modbus address
        '''
        try:
            self.name = name
            self.sn = settings['serialnumber']
            self.port = settings['port']
            self.address = settings['address']
            self.frequency = settings['measurement']
        except KeyError as ke:
            raise SensorConfigError('YAML missing required sensor setting')

        #Serial settings
        self.rs = 'RS485'
        self.duplex = 'half'
        self.resistors = 0
        self.bias = 0

        #Define characteristics of this sensor
        #Random guess at what might be a maximum sample frequency...
        self.maxfrequency = 5  #Maximum frequency in seconds the sensor can be polled

        #Setup measurement
        self.comm =  serial.Serial(
                settings['port'],
                1200,
                serial.SEVENBITS,
                serial.PARITY_EVEN,
                timeout=0)

        #Initialize data structure
        # **This should be more specific eventually...
        self.data = {'raw':[]} #Empty data dictionary

    def measure(self):
        '''
        Read in data using SDI-12 protocol
        Warning: Timing here is critical 
        Reading buffer too early will result in missed data.
        '''
        #Wake the sensor with a custom break
        self.comm.baudrate = 600
        bc = '\0'
        self.comm.write(bc.encode('utf-8'))
        time.sleep(0.04)
        self.comm.baudrate = 1200
        
        dt = datetime.datetime.now()

        #Send measure command
        mcmd = self.address + 'M!'
        self.comm.write(mcmd.encode('utf-8'))

        #Read in sensor response 
        time.sleep(0.15)
        dbytes = self.comm.in_waiting
        mtime = self.comm.read(dbytes).decode('utf-8')

        #Send D command
        dcmd = self.address+'D0!'
        self.comm.write(dcmd.encode('utf-8'))

        #Read in raw data
        # ** Parse this as necessary
        time.sleep(0.3)
        dbytes = self.comm.in_waiting
        data = self.comm.read(dbytes).decode('utf-8')

        #Store data to RAM
        self.data['raw'].append((dt,data))

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
