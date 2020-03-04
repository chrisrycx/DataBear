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
import databear.process as process
from databear import sensorfactory
import yaml
import time #For sleeping during execution
import csv
import sys #For command line args

#-------- Logger Initialization and Setup ------
class DataLogger:
    '''
    A data logger
    '''
    def __init__(self,config):
        '''
        Initialize a new data logger
        Input (various options)
        - string corresponding to name of logger (enables manual config for testing)
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

            #Create output file
            self.csvfile = open(config + '.csv','w',newline='')
            self.csvwrite = csv.DictWriter(self.csvfile,['dt','measurement','value','sensor'])
            self.csvwrite.writeheader()


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

            config = yaml.load(configyaml)

        datalogger = config['datalogger']
        loggersettings = datalogger['settings']
        sensors = config['sensors']
        
        self.name = datalogger['name']
        
        #Configure logger
        for sensor in sensors:
            sensorsettings = sensor['settings']
            samplefreq = sensorsettings['measurement']
            self.addSensor(sensor['sensortype'],sensor['name'],sensor['settings'])
            self.scheduleMeasurement(sensor['name'],samplefreq)

        for setting in loggersettings:
            self.scheduleStorage(setting['store'],setting['sensor'],setting['frequency'])

        #Create output file
        self.csvfile = open(datalogger['name']+'.csv','w',newline='')
        self.csvwrite = csv.DictWriter(self.csvfile,['dt','measurement','value','sensor'])
        self.csvwrite.writeheader()

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
        m = self.sensors[sensor].measure
        self.logschedule.every(frequency).do(m)
        
    def scheduleStorage(self,name,sensor,frequency):
        '''
        Schedule when storage takes place
        '''
        s = self.storeMeasurement
        self.logschedule.every(frequency).do(s,name,sensor,'sample')

    def storeMeasurement(self,name,sensor,process):
        '''
        Store measurement data according to process.
        - process is fixed at 'sample' for now.
        Deletes any unstored data.
        '''
        if not self.sensors[sensor].data[name]:
            #No data stored
            return

        #Extract data to be stored
        #TODO
        #self.sensors[sensor].cleardata(name)
        
        #Process data
        storedata = process.calculate(process,data,storetime)

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
        while True:
            try:
                self.logschedule.run_pending()
                sleeptime = self.logschedule.idle_seconds
                if sleeptime > 0:
                    time.sleep(sleeptime)
            except KeyboardInterrupt:
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








