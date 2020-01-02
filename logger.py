'''
Data Logger

 - Components:
    -- Measure
        - Measure each configured sensor
        - Complete measurements at sample frequency
    -- Store
        - Process the measurements: max, min, avg
        - Store data in database at storage frequency

 - General Algorithm
    1. Initialization
        - Read any configuration files
        - Initialize sensor objects for measurement
    2. Measure
        - Check clock for measure time
            - Measure sensors
            - Store values in working memory
    3. Store
        - Check clock for storage time
            - Process measurements
            - Store in database 
'''

import schedule
import time #For sleeping during execution
import sensor
import csv
import sys #For command line args

#-------- Logger Initialization and Setup ------
class DataLogger:
    '''
    A data logger
    '''
    def __init__(self,logname):
        '''
        Initialize a new data logger
        Input - logname. Used with output data file
        '''
        self.name = logname
        
        self.sensors = {}
        self.measurements = [] #Form (<measurement>,<sensor>)
        self.logschedule = schedule.Scheduler()

        #Create output file
        self.csvfile = open(logname+'.csv','w',newline='')
        self.csvwrite = csv.DictWriter(self.csvfile,['dt','measurement','value','sensor'])
        self.csvwrite.writeheader()

    def addSensor(self,name,sn):
        '''
        Add a sensor to the logger
        '''
        self.sensors[name] = sensor.Sensor(name,sn)

    def addMeasurement(self,name,mtype,sensor,settings):
        '''
        Add a measurement to a sensor
        '''
        self.sensors[sensor].add_measurement(name,mtype,settings)

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
            currentdata = self.sensors[sensor].data[name][-1]
            dt = currentdata[0].strftime('%Y-%m-%d %H:%M:%S:%f')
            val = currentdata[1]
            datadict = {
                    'dt':dt,
                    'measurement':name,
                    'value':val,
                    'sensor':sensor}

            #Output row to CSV
            self.csvwrite.writerow(datadict)
            
#-------- Process command line arguments ------
#Still developing
if len(sys.argv) > 1:
    cmdarg = sys.argv[1]
    print('Command line arg: {}'.format(cmdarg))

#-------- Logger initialization --------
#Output CSV will match name passed to DataLogger
datalogger = DataLogger('myLogger')

#-------- Logger configuration ---------

#Measurement settings

#Add Sensors
#Add Measurements
#Schedule Measurement
#Schedule Storage


#-------- Run data logger -----------
while True:
    try:
        datalogger.logschedule.run_pending()
        sleeptime = datalogger.logschedule.idle_seconds
        if sleeptime > 0:
            time.sleep(sleeptime)

    except KeyboardInterrupt:
        break

#Shut down logger
datalogger.csvfile.close()





