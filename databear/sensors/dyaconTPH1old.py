'''
Dyacon TPH-1 Sensor
This version is the older rev with no high resolution registers
- Sensor Interface V0.1

'''

import datetime
import minimalmodbus as mm
from databear.errors import MeasureError, SensorConfigError

class dyaconTPH:
    interface_version = '1.0'
    hardware_settings = {
        'serial':'RS485',
        'duplex':'half',
        'resistors':1,
        'bias':1
    }
    def __init__(self,name,settings):
        '''
        Create a new Dyacon TPH sensor
        Inputs
            - Name for sensor
            - settings['serialnum'] = Serial Number
            - settings['address'] = Sensor modbus address
        '''
        try:
            self.name = name
            self.sn = settings['serialnumber']
            self.address = settings['address']
            self.interval = settings['measure_interval']
        except KeyError as ke:
            raise SensorConfigError('YAML missing required sensor setting')

        #Define characteristics of this sensor
        self.min_interval = 1  #Minimum interval that sensor can be polled

        #Define measurements
        airT = {'name':'airT','register':201}
        rh = {'name':'rh','register':202}
        bp = {'name':'bp','register':203}
        self.measurements = [airT,rh,bp]

        #Initialize data structure
        self.data = {'airT':[],'rh':[],'bp':[]} #Empty data dictionary
        self.connected = False

    def connect(self,port):
        if not self.connected:
            self.port = port
            self.comm = mm.Instrument(self.port,self.address)
            self.comm.serial.timeout = 0.3
            self.connected = True

    def measure(self):
        '''
        Read in data using modbus
        '''
        fails = {} #keep track of measurement failures
        for measure in self.measurements:
            dt = datetime.datetime.now()
            timestamp = dt.strftime('%Y-%m-%d %H:%M:%S %f')
            
            try:
                val = self.comm.read_register(measure['register'],signed=True)
                val = val/10

                #Output results for testing
                print('{} - Measure {}: {}, value= {}'.format(
                    self.name,
                    measure['name'],
                    timestamp,
                    val))

                self.data[measure['name']].append((dt,val))
            except mm.NoResponseError as norsp:
                fails[measure['name']] = 'No response from sensor'
        #Raise a measurement error if a fail is detected
        if len(fails)>0:
            failnames = list(fails.keys())
            raise MeasureError(self.name,failnames,fails)
    
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
