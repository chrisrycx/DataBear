'''
Defines a measurement method factory
and different specific measurement
methods

Specific method interface:
- name
- units (?)
- settings
- measure() --> (datetime,value)

and Measurement classes to create
an abstract representation of a sensor that can
measure in different ways and temporarily store data.

This attempts to use a Factory Pattern to establish
the measure() method associated with a measurement.
I think it is only partially implemented though.
'''

import serial
import minimalmodbus as mm
import re #Used to parse serial data
import datetime

class measureFactory:
    '''
    Outputs measurement method objects
    '''
    def __init__(self):
        self._measuremethods = {}

    def register_measuremethod(self,measuretype,measuremethod):
        self._measuremethods[measuretype] = measuremethod

    def get_measuremethod(self,measuretype,name,settings):
        #Note: .get method on dictionary will return none if not found
        measuremethod = self._measuremethods.get(measuretype)
        if not measuremethod:
            #Evaluates true if measuremethod is none
            raise ValueError(measuremethod)
        
        return measuremethod(name,settings)

#Instantiate measureFactory for use
factory = measureFactory()

class measureModbus:
    '''
    A class to measure Modbus sensors
    '''
    def __init__(self,name,settings):
        '''
        Set up connection and modbus parameters for measurement
        Inputs
            - name
            - settings - dictionary with settings
        Required Settings:
        port - hardware port (string)
        address - sensor address (int)
        register - register associated with measurement (int)
        regtype - 'float' or 'int'
        timeout - length of time waiting for response (float)
        '''
        self.settings = settings #Useful if all settings needed somewhere
        self.name = name
        self.register = settings['register']
        self.regtype = settings['regtype']
        self.port = settings['port']
        self.address = settings['address']
        self.comm = mm.Instrument(self.port,self.address)
        self.comm.serial.timeout = settings['timeout'] #Change default response timeout

    def measure(self):
        '''
        Read a modbus sensor register according
        to register type.
        '''
        dt = datetime.datetime.now()
        if self.regtype=='float':
            val = self.comm.read_float(self.register)
        elif self.regtype=='integer':
            val = self.comm.read_register(self.register)
        else: 
            val = -999
        
        return (dt,val)

#Register method with factory
factory.register_measuremethod('modbus',measureModbus)

class measureStream:
    '''
    A class to measure streaming serial sensors
    '''
    def __init__(self,name,settings):
        '''
        Set up connection and define data
        
        Inputs
            - name
            - settings - dictionary with settings
        Required Settings:
        port - hardware port (string)
        baud - baud rate (int)
        dataRE - A regular expression to extract data from string (string)
        timeout - length of time waiting for response (float)
        '''
        self.settings = settings #Useful if all settings needed somewhere
        self.name = name
        self.port = settings['port']
        self.baud = settings['baud']
        self.timeout = settings['timeout']
        self.comm = serial.Serial(self.port,self.baud,timeout=self.timeout)
        self.dataRE = re.compile(settings['dataRE'])

    def measure(self):
        '''
        Read incoming data on the port and extract
        latest measurement.
        '''
        dt = datetime.datetime.now()

        dbytes = self.comm.in_waiting
        #print('Bytes in buffer: {}'.format(dbytes))
        rawdata = self.comm.read(dbytes).decode('utf-8')

        #Find last regular expression match in raw data
        val = self.dataRE.findall(rawdata)[-1]

        #Convert to a float
        val = float(val)

        return (dt,val)

factory.register_measuremethod('stream',measureStream)
