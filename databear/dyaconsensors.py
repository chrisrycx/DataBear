'''
Dyacon sensor classes that conform to interface defined
in sensor.py
'''

import datetime
import minimalmodbus as mm

class dyaconTPH:
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
        self.name = name
        self.sn = settings['serialnum']
        self.port = settings['port']
        self.address = settings['address']
        self.frequency = settings['frequency']

        #Define characteristics of this sensor
        self.sensor_type = 'polled'
        self.maxfrequency = 1  #Maximum frequency in seconds the sensor can be polled

        #Define measurements
        airT = {'name':'airT','register':210,'regtype':'float'}
        rh = {'name':'rh','register':212,'regtype':'float'}
        bp = {'name':'bp','register':214,'regtype':'float'}
        self.measurements = [airT,rh,bp]

        #Setup measurement
        self.comm = mm.Instrument(self.port,self.address)
        self.comm.serial.timeout = 0.3

        #Initialize data structure
        self.data = {'airT':[],'rh':[],'bp':[]} #Empty data dictionary

    def measure(self):
        '''
        Read in data using modbus
        '''
        for measure in self.measurements:
            dt = datetime.datetime.now()
            val = self.comm.read_float(measure['register'])

            #Output results for testing
            timestamp = dt.strftime('%Y-%m-%d %H:%M:%S %f')
            print('Measure {}: {}, value= {}'.format(measure['name'],timestamp,val))

            self.data[measure['name']].append((dt,val))


    def cleardata(self,name):
        '''
        Clear data values for a particular measurement
        '''
        self.data[name] = []
