'''
Base class for DataBear sensors
'''
from databear.errors import SensorConfigError, MeasureError

class Sensor:
    interface_version = '1.1'
    hardware_settings = {}
    measurements = [] #List of measurement names
    units = {} #List of units associated with measurement names
    measurement_description = {}
    temporal_resolution = 'minutes' #Options: minutes, seconds, microseconds
    def __init__(self,name,sn,address):
        '''
        Create a new sensor
        Inputs
        - name (string): sensor name
        - sn (string): serial number
        - address (int): default 0
        - interval (float): measurement interval in seconds
        '''
        try:
            self.name = name
            self.sn = sn
            self.address = address
        except KeyError as ke:
            raise SensorConfigError('YAML missing required sensor setting')

        #Define characteristics of this sensor
        self.configid = None
        self.min_interval = 0  #Minimum interval that sensor can be polled

        #Initialize data structure
        self.data = {}
        for measure_name in self.measurements:
            self.data[measure_name] = []
        
        self.connected = False
    
    def __str__(self):
        '''
        Standardized way to print sensor:
        <Sensor Name> - <measure name>:(dt,val), ...
        '''
        output = self.name + '\n' #Initialize

        #Get current values
        currentdata = self.getcurrentdata()
        #Create output string
        for m,v in currentdata.items():
            if v:
                dtstr = v[0].strftime('%Y-%m-%d %H:%M:%S:%f')
                output = output + '{}: {}, {}\n'.format(m,dtstr,v[1])
            else:
                output = output + '{}: No Data\n'.format(m)

        return output

    def connect(self,port):
        pass

    def measure(self):
        pass
    
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
        try:
            data = self.data[name]
            for val in data:
                if (val[0]>=startdt) and (val[0]<enddt):
                    output.append(val)
            return output
        except KeyError as ke:
            print(name + " missing from " + data)
            raise MeasureError(name, [], "name missing from dictionary")

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