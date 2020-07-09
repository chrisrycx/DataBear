'''
Dyacon WSD-1 Sensor
Initial sensor interface for Dyacon WSD-1 sensor
- Tested platform(s): Dyacon MDL
- Interface Version: 0.1

'''

import datetime
import minimalmodbus as mm
from databear.errors import MeasureError, SensorConfigError

class dyaconWSD1:
    #Inherit from "modbus sensor class"?
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
            self.scalefactor = settings['scalefactor']
        except KeyError as ke:
            raise SensorConfigError('YAML missing required sensor setting')

        #Serial settings
        self.rs = 'RS485'
        self.duplex = 'half'
        self.resistors = 1
        self.bias = 1

        #Define characteristics of this sensor
        #self.sensor_type = 'polled'   PJD
        self.sensortype = 'modbus'
        self.maxfrequency = 1  #Maximum frequency in seconds the sensor can be polled

        #Define measurements
        WS = {'name':'WindSpeed','register':201,'regtype':'integer'}
        WD = {'name':'WindDir','register':202,'regtype':'integer'}
        self.measurements = [WS,WD]

        #Setup measurement
        self.comm = mm.Instrument(self.port,self.address)
        self.comm.serial.timeout = 0.3

        #Initialize data structure
        self.data = {'WindSpeed':[],'WindDir':[]} #Empty data dictionary

    def measure(self):
        '''
        Read in data using modbus
        '''
        fails = {} #keep track of measurement failures
        for measure in self.measurements:
            dt = datetime.datetime.now()
            timestamp = dt.strftime('%Y-%m-%d %H:%M:%S %f')
            
            try:
                #val = self.comm.read_float(measure['register'])
                val = self.comm.read_register(measure['register'])
                val = val*self.scalefactor   # WSD1 outputs in m/s or deg *10
                val = str(format(val,'.1f'))  # apply scale factor causes messy precision issues. Force precision and make string. This may cause problems later.
                #Output results for testing
               # print('Measure {}: {}, value= {}'.format(measure['name'],timestamp,val))

                self.data[measure['name']].append((dt,val))
            except mm.NoResponseError as norsp:
                fails[measure['name']] = 'No response from sensor'
        #Raise a measurement error if a fail is detected
        if len(fails)>0:
            failnames = list(fails.keys())
            raise MeasureError(failnames,fails)

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
