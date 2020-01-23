'''
Defines a sensor class

'''

import databear.measure as measure

class Sensor:
    def __init__(self,name,serialnum,measurements):
        '''
        Create a new sensor
        Inputs
            - A name and serial number for the sensor
            - Measurements: A list of dictionaries
                    [{'name':<measurename>,'method':<measuremethod>,<other settings>},...]
        '''
        self.name = name
        self.sn = serialnum
        self.measurements = {} #
        self.data = {} #Empty data dictionary

        #Load each measurement
        for measure in measurements:
            mname = measure.pop('name') #Returns name and removes from list
            self.add_measurement(mname,measure) #Remaining settings get sent to add measurement

    def add_measurement(self,name,settings):
        '''
        Add a new measurement to the sensor
        Inputs
            - name of measurement
            - mtype: type of measurement
            - settings: dictionary of settings
        '''
        self.measurements[name] = measure.factory.get_measuremethod(settings['method'],name,settings)
        self.data[name] = []

    def change_settings(self,name,settings):
        '''
        Changes an existing measurement by deleting measurement object
        and recreating with new settings
        '''
        del self.measurements[name]
        self.measurements[name] = measure.factory.get_measuremethod(settings['method'],name,settings)

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







