'''
Sensor.py
Defines Sensor and Measurement classes to create
an abstract representation of a sensor that can
measure in different ways and temporarily store data.

This attempts to use a Factory Pattern to establish
the measure() method associated with a measurement.
I think it is only partially implemented though.

'''

#Dependencies for different measurements
import serial
import minimalmodbus as mm
import re #Used to parse serial data
import datetime

class Sensor:
    def __init__(self,name,serialnum):
        '''
        Create a new sensor
        Inputs
            - A name and serial number for the sensor
        '''
        self.name = name
        self.sn = serialnum
        self.measurements = {} #A dictionary of measurement objects
        self.data = {} #Empty data dictionary

    def add_measurement(self,name,mtype,settings):
        '''
        Add a new measurement to the sensor
        Inputs
            - name of measurement
            - mtype: type of measurement
            - settings: dictionary of settings
        '''
        if mtype == 'modbus':
            self.measurements[name] = measureModbus(name,settings)
        elif mtype == 'streaming':
            self.measurements[name] = measureStream(name,settings)
        else:
            raise ValueError(mtype)

        self.data[name] = []

    def measure(self,name):
        '''
        Perform a measurement and puts result in data dictionary
        Input - name of measurement
        
        '''
        try:
            mdata = self.measurements[name].measure()
            self.data[name].append(mdata)
            timestamp = mdata[0].strftime('%Y-%m-%d %H:%M:%S %f')
            print('{}: {}={}'.format(timestamp,name,mdata[1]))
        except:
            print('Problem with {} {} measurement'.format(self.name,name))

        

    def cleardata(self,name):
        '''
        Clear data values for a particular measurement
        '''
        self.data[name] = []


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





