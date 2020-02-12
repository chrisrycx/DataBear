'''
Dyacon Sensor Classes
- Platform: Windows
- Connection: USB-RS485
- Interface: Conform with current...???

'''

import datetime

#Imports for SDI12 sensors
import serial
import time
import re

#Imports for modbus sensors
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
        self.sn = settings['serialnumber']
        self.port = settings['port']
        self.address = settings['address']
        self.frequency = settings['measurement']

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


class dyaconWSD2:
    def __init__(self,name,settings):
        '''
        Create a new Dyacon WSD-2 sensor
        This sensor is SDI-12 and the protocol
        is implemented via pySerial with a helper function
        Inputs
            - Name for sensor
            - settings['serialnumber'] = Serial Number
            - settings['port'] = Serial com port
            - settings['address'] = Sensor SDI-12 address
            - settings['measurement'] = Measurement frequency
        '''
        self.name = name
        self.sn = settings['serialnumber']
        self.port = settings['port']
        self.address = settings['address']
        self.frequency = settings['measurement']

        #Define characteristics of this sensor
        self.sensor_type = 'polled'
        self.maxfrequency = 5  #Maximum frequency in seconds the sensor can be polled

        #Define measurements
        self.data={'speed':[]}

        #Setup measurement
        self.comm =  serial.Serial(settings['port'],1200,serial.SEVENBITS,serial.PARITY_EVEN,timeout=0)


    def measure(self):
        '''
        Read in data using SDI-12 protocol
        Warning: Timing here is critical 
        Reading buffer too early will result in missed data.
        '''
        #Wake the sensor with a custom break
        '''
        self.comm.baudrate = 600
        bc = '\0'
        self.comm.write(bc.encode('utf-8'))
        time.sleep(0.04)
        self.comm.baudrate = 1200
        '''
        #print('Measuring')
        dt = datetime.datetime.now()

        #Windows
        self.comm.send_break(0.02)
        time.sleep(0.016)
        self.comm.send_break(0.016)
        time.sleep(0.016)

        #Send measure command
        mcmd = self.address + 'M!'
        self.comm.write(mcmd.encode('utf-8'))  #Also tried UTF-8

        #Read in sensor response. WSD-2 will return zero, but read in to clear buffer
        time.sleep(0.1)
        dbytes = self.comm.in_waiting
        mtime = self.comm.read(dbytes).decode('utf-8')
        #print(mtime)

        #Send D command
        dcmd = self.address+'D0!'
        self.comm.write(dcmd.encode('utf-8'))

        #Read in raw data
        time.sleep(0.3)
        dbytes = self.comm.in_waiting
        #print('Data bytes: {}'.format(dbytes))
        data = self.comm.read(dbytes).decode('utf-8')

        #Output results for testing
        timestamp = dt.strftime('%Y-%m-%d %H:%M:%S %f')
        print('Measure SDI12: {}, value= {}'.format(timestamp,data))

        #Store in RAM
        self.data['speed'].append((dt,data))   


    def cleardata(self,name):
        '''
        Clear data values for a particular measurement
        '''
        self.data[name] = []


