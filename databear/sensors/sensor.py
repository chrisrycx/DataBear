'''
Base class for DataBear sensors
'''
from databear.errors import SensorConfigError, MeasureError
import datetime
import time

class Sensor:
    interface_version = '1.2'
    hardware_settings = {}
    measurements = [] #List of measurement names
    units = {} #List of units associated with measurement names
    measurement_description = {}
    min_interval = 1  #Minimum interval that sensor can be polled
    uses_portlock = False # Set to true in all sensor classes that require a portlock (modbus sensors)
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


class BusSensor(Sensor):
    '''
    A base class for a sensor that can be part of
    a bus network architecture.
    '''
    def __init__(self,name,sn,address):
        '''
        Override base class to add port lock
        '''
        super().__init__(name,sn,address)
        self.portlock = None
    
    def connect(self,port,portlock):
        '''
        Set up portlock and connection
        '''
        self.portlock = portlock
    
    def startMeasure(self):
        '''
        Begin a concurrent measurement
        Return the wait time between start and read
        '''
        return 0

    def readMeasure(self,starttime):
        '''
        Read measurement from sensor
        '''
        pass

    def measure(self):
        '''
        Coordinate start and read measure with
        port locks on the bus
        '''
        dt = datetime.datetime.now()
        try:
            #The start measurement sequence
            self.portlock.acquire()
            s = self.startMeasure()
            self.portlock.release()

            #Wait s then read
            time.sleep(s)
            self.portlock.acquire()
            self.readMeasure(dt)
            self.portlock.release()
            
        except:
            #Unlock the port if any exception
            self.portlock.release()
            #Raise again so that the exception is logged
            raise
        
        
        
        
    
