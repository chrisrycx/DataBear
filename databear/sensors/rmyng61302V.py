'''
RM Young 61302V Barometric Pressure sensor
'''

import datetime
from databear.errors import MeasureError, SensorConfigError
from databear.sensors import sensor
import serial

class rmyoungBP(sensor.Sensor):
    hardware_settings = {
        'serial':'RS232',
        'duplex':'full',
        'resistors':0,
        'bias':0
    }
    def __init__(self,name,sn,address,interval):
        '''
        Create a new RM Young BP sensor
        '''
        super().__init__(name,sn,address,interval)

        #Define characteristics of this sensor
        #Random guess at what might be a maximum sample frequency...
        self.min_interval = 5  #minimum interval in seconds the sensor can be polled
        self.connected = False

        #Initialize data structure
        self.data = {'bp':[]}

    def connect(self,port):
        if not self.connected:
            self.port = port
            self.comm = serial.Serial(self.port,9600,timeout=0.5)
            self.comm.reset_input_buffer()
            self.connected = True

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

    

    


    