'''
Dyacon Sensor WSD-2
Wind speed and direction sensor with SDI12 interface.

Classes:
dyaconWSD2
- Platforms: Windows, Linux
- Tested hardware: USB-RS485, Dyacon MDL serial module
- Interface: DataBear Sensor Interface V0

'''

import datetime

#Imports for SDI12 sensors
import serial
import time
import re

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

        #Serial settings
        self.rs = 'RS485'
        self.duplex = 'half'
        self.resistors = 0
        self.bias = 0

        #Define characteristics of this sensor
        #maxfrequency: Maximum frequency in seconds the sensor can be polled
        self.sensor_type = 'polled'
        self.maxfrequency = 5  

        #Define measurements
        self.data={'speed':[],'direction':[]}

        #Setup measurement
        self.comm =  serial.Serial(
                settings['port'],
                1200,
                serial.SEVENBITS,
                serial.PARITY_EVEN,
                timeout=0)


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

        #Windows only
        #self.comm.send_break(0.02)
        #time.sleep(0.016)
        #self.comm.send_break(0.016)
        #time.sleep(0.016)

        #Send measure command
        mcmd = self.address + 'M!'
        self.comm.write(mcmd.encode('utf-8'))  #Also tried UTF-8

        #Read in sensor response. 
        #WSD-2 will return zero, but read in to clear buffer
        time.sleep(0.15)
        dbytes = self.comm.in_waiting
        mtime = self.comm.read(dbytes).decode('utf-8')
        print('Measure time: {}'.format(mtime))

        #Send D command
        dcmd = self.address+'D0!'
        self.comm.write(dcmd.encode('utf-8'))

        #Read in raw data
        time.sleep(0.3)
        dbytes = self.comm.in_waiting
        print('Raw data bytes: {}'.format(dbytes))
        data = self.comm.read(dbytes).decode('utf-8')

        #Output results for testing
        timestamp = dt.strftime('%Y-%m-%d %H:%M:%S %f')
        print('Measure SDI12: {}, data= {}'.format(timestamp,data[:-2]))

        #Parse incoming data - pattern: 0+4.5+284.5\r\n
        dataRE = r'\d+\.\d+'  #Find all decimals
        dvals = re.findall(dataRE,data)

        # Store in RAM
        speed = float(dvals[0])
        direction = float(dvals[1])
        self.data['speed'].append((dt,speed))
        self.data['direction'].append((dt,direction))   


    def cleardata(self,name):
        '''
        Clear data values for a particular measurement
        '''
        self.data[name] = []


