'''
RM Young 61302V Barometric Pressure sensor
- DataBear Sensor Interface: V1.0
'''

import datetime
from databear.errors import MeasureError, SensorConfigError
import serial

class rmyoungBP:
    interface_version = '1.0'
    hardware_settings = {
        'serial':'RS232',
        'duplex':'full',
        'resistors':0,
        'bias':0
    }

    def __init__(self,name,settings):
        '''
        Create a new Dyacon TPH sensor
        Inputs
        - name: string - name for sensor
        - settings: dictionary
            settings['serialnum'] = Serial Number 
            settings['measure_interval'] = Sensor measurement interval sec 
        '''
        try:
            self.name = name
            self.sn = settings['serialnumber']
            self.interval = settings['measure_interval']
        except KeyError as ke:
            raise SensorConfigError('YAML missing required sensor setting')


        #Define characteristics of this sensor
        #Random guess at what might be a maximum sample frequency...
        self.min_interval = 5  #minimum interval in seconds the sensor can be polled
        self.timeout = 0.5
        self.connected = False

        #Initialize data structure
        self.data = {'bp':[]}

    def connect(self,port):
        if not self.connected:
            self.port = port
            self.comm = serial.Serial(self.port,9600,timeout=self.timeout)
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
            print('RMY - {}, value={}'.format(dt.strftime('%M:%S:%f'),bpnum))

    def getcurrentdata(self):
        '''
        Return most recent data from sensor
        Output:
            {'name':(dt,val),'name2'...}
        Return None if no data for particular measurement
        '''
        currentdata = {}
        for key,val in self.data.items():
            try:
                currentdata[key]=val[-1]
            except IndexError:
                #Assign none if there is nothing in list
                currentdata[key]=None

        return currentdata

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