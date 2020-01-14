'''
Defines a sensor class

'''

import databear.measure as measure

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
        self.measurements[name] = measure.factory.get_measuremethod(mtype,name,settings)
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







