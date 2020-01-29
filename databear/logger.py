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
import databear.sensor as sensor
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
        Input
          - configuration: string or dictionary
            If config is a string it should be
            the path to the yaml configuration file.
            If config is a dictionary, it should have
            the same form as an imported yaml file.
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
        
        #Initialize properties
        self.sensors = {}
        self.loggersettings = [] #Form (<measurement>,<sensor>)
        self.logschedule = schedule.Scheduler()

        #Configure logger
        for sensor in sensors:
            self.addSensor(sensor['name'],sensor['serialnumber'],sensor['measurements'])

        for setting in loggersettings:
            self.scheduleMeasurement(setting['measurement'],setting['sensor'],setting['sample'])
            self.scheduleStorage(setting['measurement'],setting['sensor'],setting['store'])

        #Create output file
        self.csvfile = open(datalogger['name']+'.csv','w',newline='')
        self.csvwrite = csv.DictWriter(self.csvfile,['dt','measurement','value','sensor'])
        self.csvwrite.writeheader()

    def addSensor(self,name,sn,measurements):
        '''
        Add a sensor to the logger
        '''
        self.sensors[name] = sensor.Sensor(name,sn,measurements)

    def scheduleMeasurement(self,name,sensor,frequency):
        '''
        Schedule a measurement
        Frequency is seconds
        '''
        m = self.sensors[sensor].measure
        self.logschedule.every(frequency).do(m,name)
        
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

        if process=='sample':
            for value in self.sensors[sensor].data[name]:
                dt = value[0].strftime('%Y-%m-%d %H:%M:%S:%f')
                val = value[1]
                datadict = {
                    'dt':dt,
                    'measurement':name,
                    'value':val,
                    'sensor':sensor}
            
                #Output row to CSV
                self.csvwrite.writerow(datadict)
            
        self.sensors[sensor].cleardata(name)

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








