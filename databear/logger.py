'''
Data Logger

 - Components:
    -- Measure
        - Measure each configured sensor
        - Complete measurements at sample frequency
    -- Store
        - Process the measurements: max, min, avg
        - Store data in database at storage frequency
** Need more documentation here...

'''

import databear.schedule as schedule
import databear.process as processdata
from databear import sensorfactory
from databear.errors import DataLogConfigError, MeasureError
from datetime import timedelta
import concurrent.futures
import yaml
import time #For sleeping during execution
import csv
import sys #For command line args
import logging



#-------- Logger Initialization and Setup ------
class DataLogger:
    '''
    A data logger
    '''
    #Error logging format
    errorfmt = '%(asctime)s %(levelname)s %(lineno)s %(message)s'

    def __init__(self,config):
        '''
        Initialize a new data logger
        Input (various options)
        - string corresponding to name of logger 
          (enables manual config for testing)
        - path to yaml config file (must have .yaml)
        - dictionary with configuration
          
        '''
        #Initialize properties
        self.sensors = {}
        self.loggersettings = [] #Form (<measurement>,<sensor>)
        self.logschedule = schedule.Scheduler()

        #Determine what input is
        if (isinstance(config,dict)) or (config[-4:]=='yaml'):
            #Pass dictionary to loadconfig
            self.loadconfig(config)
        else:
            #Name assumed to be defined by input string
            self.name = config
            logging.basicConfig(
                format=DataLogger.errorfmt,
                filename=self.name+'_error.log')
            
            #Create output file
            self.csvfile = open(config + '.csv','w',newline='')
            self.csvwrite = csv.DictWriter(self.csvfile,['dt','measurement','value','sensor'])
            self.csvwrite.writeheader()

            #Create threadpool with default workers
            self.workerpool = concurrent.futures.ThreadPoolExecutor()

    def loadconfig(self,config):
        '''
        Load configuration file
        Input options
        - path to yaml
        - dictionary with configuration
        '''

        if isinstance(config,str):
            #Import configuration from yaml
            with open(config,'rt') as yin:
                configyaml = yin.read()

            config = yaml.safe_load(configyaml)

        datalogger = config['datalogger']
        loggersettings = datalogger['settings']
        sensors = config['sensors']
        
        self.name = datalogger['name']

        #Set up error logging
        logging.basicConfig(
                format=DataLogger.errorfmt,
                filename=self.name+'_error.log')
        
        #Configure logger
        for sensor in sensors:
            try:
                sensorsettings = sensor['settings']
            except TypeError as tp:
                raise DataLogConfigError(
                'YAML configured wrong. Sensor block missing dash (-)')
            
            samplefreq = sensorsettings['measurement']
            self.addSensor(sensor['sensortype'],sensor['name'],sensor['settings'])
            self.scheduleMeasurement(sensor['name'],samplefreq)

        for setting in loggersettings:
            try:
                self.scheduleStorage(
                    setting['store'],
                    setting['sensor'],
                    setting['frequency'],
                    setting['process'])
            except TypeError as tp:
                raise DataLogConfigError(
                'YAML configured wrong. Logger setting missing dash (-)')
            except DataLogConfigError:
                print('in config error?')
                raise


            

        #Create output file
        self.csvfile = open(datalogger['name']+'.csv','w',newline='')
        self.csvwrite = csv.DictWriter(self.csvfile,['dt','measurement','value','sensor'])
        self.csvwrite.writeheader()

        #Create threadpool
        self.workerpool = concurrent.futures.ThreadPoolExecutor(max_workers=len(sensors))

    def addSensor(self,sensortype,name,settings):
        '''
        Add a sensor to the logger
        '''
        self.sensors[name] = sensorfactory.factory.get_sensor(sensortype,name,settings)

    def scheduleMeasurement(self,sensor,frequency):
        '''
        Schedule a measurement
        Frequency is seconds
        '''
        #Check frequency against max
        if frequency < self.sensors[sensor].maxfrequency:
            raise DataLogConfigError('Logger frequency exceeds sensor max')
        
        #Schedule measurement
        m = self.doMeasurement
        self.logschedule.every(frequency).do(m,sensor)
    
    def doMeasurement(self,sensor,storetime,lasttime):
        '''
        Perform a measurement on a sensor
        Inputs
        - Sensor name
        - storetime and lasttime are not currently used here
          but are passed by Schedule when this function is called.
        '''
        mfuture = self.workerpool.submit(self.sensors[sensor].measure)
        mfuture.add_done_callback(self.endMeasurement)
        
    def endMeasurement(self,mfuture):
        '''
        A callback after measurement is complete
        Use to log any exceptions that occurred
        input: mfuture - a futures object that gets passed when complete
        '''
        #Retrieve exception. Returns none is no exceptions
        merrors = mfuture.exception()

        #Log exceptions
        if merrors:
            for m in merrors.measurements:
                logging.error('{}:{} - {}'.format(
                        merrors.sensor,
                        m,
                        merrors.messages[m]))


    def scheduleStorage(self,name,sensor,frequency,process):
        '''
        Schedule when storage takes place
        '''
        #Check storage frequency doesn't exceed measurement frequency
        if frequency < self.sensors[sensor].frequency:
            raise DataLogConfigError('Storage frequency exceeds sensor measurement frequency')

        s = self.storeMeasurement
        #Note: Some parameters for function supplied by Job class in Schedule
        self.logschedule.every(frequency).do(s,name,sensor,process)

    def storeMeasurement(self,name,sensor,process,storetime,lasttime):
        '''
        Store measurement data according to process.
        Inputs
        - name, sensor
        - process: A valid process type
        - storetime: datetime of the scheduled storage
        - lasttime: datetime of last storage event
        - Process = 'average','min','max','dump','sample'
        - Deletes any data associated with storage after saving
        '''

        #Deal with missing last time on start-up
        #Set to storetime - 1 day to ensure all data is included
        if not lasttime:
            lasttime = storetime - timedelta(1)

        #Get datetimes associated with current storage and prior
        data = self.sensors[sensor].getdata(name,lasttime,storetime)

        if not data:
            #No data found to be stored
            logging.warning(
                '{}:{} - No data available for storage'.format(sensor,name))
            return
        
        #Process data
        storedata = processdata.calculate(process,data,storetime)

        #Write to CSV
        for row in storedata:
            datadict = {
                    'dt': row[0],
                    'measurement':name,
                    'value': row[1],
                    'sensor':sensor}

            #Output row to CSV
            self.csvwrite.writerow(datadict)
            
    def run(self):
        '''
        Run the logger
        ctrl-C to stop
        '''
        print('DataBear: Logger starting - ctrl-C to stop')
        while True:
            try:
                self.logschedule.run_pending()
                sleeptime = self.logschedule.idle_seconds
                if sleeptime > 0:
                    time.sleep(sleeptime)
            except AssertionError:
                logging.error('Measurement too late, logger resetting')
                self.logschedule.reset()
            except KeyboardInterrupt:
                self.workerpool.shutdown()
                break

        #Close CSV after stopping
        self.csvfile.close()
            

#-------- Run from command line -----
if __name__ == "__main__":

    #Process command line args
    if len(sys.argv) < 2:
        print('Enter path to config file from current directory')
        exit(0)

    confpath = sys.argv[1]
    print(confpath)

    datalogger = DataLogger(confpath)

    #Run logger
    datalogger.run()








