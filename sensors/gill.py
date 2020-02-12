class Windmaster:
    def __init__(self,name,serialnum,windid,port,hz):
        '''
        Create a new windmaster sensor
        Inputs
            - Serial Number
            - ID corresponding to ID in message
            - port: Serial com port
            - hz: Rate of sensor output
        '''
        self.name = 'windmaster'
        self.sn = serialnum
        self.windid = windid
        self.hz = hz

        #Define characteristics of this sensor
        self.sensor_type = 'continuous'

        #Define measurements
        wind_x = {'name':'wind_x','dataRE':'test'}
        wind_y = {'name':'wind_y','dataRE':'test'}
        wind_z = {'name':'wind_z','dataRE':'test'}
        self.measurements = [wind_x,wind_y,wind_z]

        #Initialize data structure
        self.data = {} #Empty data dictionary

    def measure(self):
        '''

        Read in data from port and parse

        '''
        rawdata = 'TestingTesting'

        for measure in self.measurements:
            #Parse measurement data from raw data
            data = [('2020-01-30 00:00',55),('2020-01-30 00:01',55)]
            self.data[measure['name']] = data


    def cleardata(self,name):
        '''
        Clear data values for a particular measurement
        '''
        self.data[name] = []