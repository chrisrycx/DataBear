'''
The DataBear data logger
- Runs using configuration from sqlite database

'''

import databear.schedule as schedule
import databear.process as processdata
import databear.databearDB as databearDB
from databear import sensorfactory
from databear.errors import DataLogConfigError, MeasureError
from databear.databearDB import DataBearDB
from datetime import datetime, timedelta
import concurrent.futures
import threading #For IPC
import selectors #For IPC via UDP
import socket
import json
import time #For sleeping during execution
import csv
import sys #For command line args
import logging
import os
import importlib


#-------- Logger Initialization and Setup ------
class DataLogger:
    '''
    A data logger
    '''
    #Error logging format
    errorfmt = '%(asctime)s %(levelname)s %(lineno)s %(message)s'

    def __init__(self):
        '''
        Initialize a new data logger
        Input (various options)
       
        dbdriver:
            - An instance of a DB hardware driver
        '''
        #Initialize attributes
        self.sensors = {}
        self.portlocks = {}
        self.loggersettings = [] #Form (<measurement>,<sensor>)
        self.logschedule = schedule.Scheduler()

        #Load driver env var
        try:
            drivername = os.environ['DBDRIVER']
        except KeyError:
            print('DBDRIVER not set, searching for driver in CWD')
            drivername = 'dbdriver'

        #Try loading driver as a package, then path
        try:
            driver_module = importlib.import_module(drivername)
        except ImportError:
            #Try loading from path
            spec = importlib.util.spec_from_file_location("dbdriver", drivername)
            driver_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(driver_module)

        self.driver = driver_module.dbdriver()

        #Set up database connection
        self.db = DataBearDB()

        #Configure UDP socket for API
        self.udpsocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.udpsocket.bind(('localhost',62000))
        self.udpsocket.setblocking(False)
        self.sel = selectors.DefaultSelector()
        self.sel.register(self.udpsocket,selectors.EVENT_READ)
        self.listen = False
        self.messages = []

        #Set up error logging
        logging.basicConfig(
            level=20,
            format=DataLogger.errorfmt,
            filename='databear_error.log'
            )

    def register_sensors(self):
        '''
        Register all sensor classes in sensors_available with the factory
        '''
        #Get sensors from database
        module_names = self.db.sensors_available

        #Import all sensor classes
        for module_name in module_names:
            sensor_module = importlib.import_module(module_name)
            sensor_class = getattr(sensor_module,'dbsensor')

            #Register sensor with factory
            sensorfactory.factory.register_sensor(
                module_name,
                sensor_class)

    def loadconfig(self):
        '''
        Get configuration out of database and
        start sensors
        '''
        #Register available sensors
        self.register_sensors()
        
        #Get list of active sensors and logging
        sensorids = self.db.getSensorIDs(activeonly=True)
        loggingconfigs = self.db.getConfigIDs('logging',activeonly=True)
        
        #Configure logger
        for sensorid in sensorids:
            sensorsettings = self.db.getSensorConfig(sensorid)

            self.addSensor(
                sensorsettings['name'],
                sensorsettings['serial_number'],
                sensorsettings['address'],
                sensorsettings['virtualport'],
                sensorsettings['module_name'],
                sensorsettings['sensor_config_id']
                )
            self.scheduleMeasurement(
                sensorsettings['name'],
                sensorsettings['measure_interval']
                )

        for loggingid in loggingconfigs:
            storagesetting = self.db.getLoggingConfig(loggingid)
                
            self.scheduleStorage(
                loggingid,
                storagesetting['measurement_name'],
                storagesetting['sensor_name'],
                storagesetting['storage_interval'],
                storagesetting['process'])
                  
    def addSensor(self,name,sn,address,virtualport,sensortype,sensorconfigid):
        '''
        Add a sensor to the logger
        '''
        #Create sensor object
        sensor = sensorfactory.factory.get_sensor(
            sensortype,
            name,
            sn,
            address
            )
        sensor.configid = sensorconfigid

        #"Connect" virtual port to hardware using driver
        hardware_port = self.driver.connect(virtualport,sensor.hardware_settings)

        #"Connect" sensor to hardware
        #bus type ports are given thread locks
        if sensor.uses_portlock: 
            plock = self.portlocks.get(virtualport)
            if not plock:
                plock = threading.Lock()
                self.portlocks[virtualport] = plock 
            sensor.connect(hardware_port,plock)
        else:
            sensor.connect(hardware_port)

        #Add sensor to collection
        self.sensors[name] = sensor

    def stopSensor(self,name):
        '''
        Stop sensor measurement and storage
        Input - sensor name
        '''
        successflag = 0
        for job in self.logschedule.jobs:
            jobsettings = job.getsettings()
            #Extract sensor name
            if jobsettings['function'] == 'doMeasurement':
                sensorname = jobsettings['args'][0]
            elif jobsettings['function'] == 'storeMeasurement':
                sensorname = jobsettings['args'][1]

            #Cancel job if matches sensor name
            if sensorname == name:
                self.logschedule.cancel_job(job)
                logging.warning('Shutdown sensor {}'.format(name))
                successflag = 1

        return successflag
    
    def reload(self):
        successflag = True

        # First stop all current jobs
        for job in self.logschedule.jobs:
            self.logschedule.cancel_job(job)

        # Then stop workerpool threads
        self.workerpool.shutdown()

        # reload configuration, creating sensors as needed
        self.loadconfig()

        # lastly recreate workerpool based on new number of sensors
        self.workerpool = concurrent.futures.ThreadPoolExecutor(
            # use at least 1 worker
            max_workers=max(len(self.sensors),1))

        return successflag

    def scheduleMeasurement(self,sensorname,interval):
        '''
        Schedule a measurement:
        Interval is seconds
        '''
        
        #Check interval to ensure it isn't too small
        if interval < self.sensors[sensorname].min_interval:
            raise DataLogConfigError('Logger frequency exceeds sensor max')
        
        #Schedule measurement
        m = self.doMeasurement
        self.logschedule.every(interval).do(m,sensorname,interval)
    
    def doMeasurement(self,sensorname,interval,scheduled_time,last_time):
        '''
        Perform a measurement on a sensor
        Inputs
        - Sensor name
        - storetime and lasttime are not currently used here
          but are passed by Schedule when this function is called.
        '''
        #Check to see if job is on time. Skip measurement if
        #current time - scheduled time is more than the measurement interval
        dtdiff = datetime.now() - scheduled_time
        if dtdiff.total_seconds() > interval:
            #Too late, skip measurement
            logging.error('Skipping measurement for {}'.format(sensorname))
        else:
            mfuture = self.workerpool.submit(self.sensors[sensorname].measure)
            mfuture.sname = sensorname
            mfuture.add_done_callback(self.endMeasurement)
        
    def endMeasurement(self,mfuture):
        '''
        A callback after measurement is complete
        Use to log any exceptions that occurred
        input: mfuture - a futures object that gets passed when complete
        '''
        #print(self.sensors[mfuture.sname])

        #Retrieve exception. Returns none is no exceptions
        merrors = mfuture.exception()

        #Log exceptions
        if merrors:
            try:
                for m in merrors.measurements:
                    logging.error('{}:{} - {}'.format(
                            merrors.sensor,
                            m,
                            merrors.messages[m]))
            except:
                raise RuntimeError(merrors)

    def scheduleStorage(self,configid,name,sensor,interval,process):
        '''
        Schedule when storage takes place
        '''
        #Check storage frequency doesn't exceed measurement frequency
        if interval < self.sensors[sensor].min_interval:
            raise DataLogConfigError('Storage frequency exceeds sensor measurement frequency')

        s = self.storeMeasurement
        #Note: Some parameters for function supplied by Job class in Schedule
        self.logschedule.every(interval).do(s,configid,name,sensor,process,interval)

    def storeMeasurement(self,logconfigid,name,sensor,process,interval,scheduled_time,last_time):
        '''
        Store measurement data according to process.
        Inputs
        - logconfigid for database
        - name: measurement name
        - sensor: sensor name
        - process: A valid process type
        - interval: storage interval (used to determine temporal resolution)
        - storetime: datetime of the scheduled storage
        - lasttime: datetime of last storage event
        - Process = 'average','min','max','dump','sample'
        '''

        #Deal with missing last time on start-up
        #Set to storetime - 1 day to ensure all data is included
        if not last_time:
            last_time = scheduled_time - timedelta(1)

        #Get datetimes associated with current storage and prior
        data = self.sensors[sensor].getdata(name,last_time,scheduled_time)

        if not data:
            #No data found to be stored
            logging.warning(
                '{}:{} - No data available for storage'.format(sensor,name))
            return
        
        #Process data
        storedata = processdata.calculate(process,data,scheduled_time)

        #Write data to database
        if interval < 1:
            tresolution = 'microseconds'
        elif interval < 60:
            tresolution = 'seconds'
        else:
            tresolution = 'minutes'

        #Include microseconds if dump is used
        if process == 'Dump':
            tresolution = 'microseconds'

        for row in storedata:
            dtstr = row[0].isoformat(sep=' ',timespec=tresolution)
            value = row[1]

            self.db.storeData(
                dtstr,
                value,
                self.sensors[sensor].configid,
                logconfigid,
                0)
            
    def listenUDP(self):
        '''
        Listen on UDP socket
        '''
        while self.listen:
            #Check for UDP comm
            event = self.sel.select(timeout=1)
            if event:
                self.readUDP()

    def readUDP(self):
        '''
        Read message, respond, add any messages
        to the message queue
        Message should be JSON
        {'command': <cmd> , 'arg': <optional argument>}

        Commands
        - status
        - getdata
            -- argument: sensor name
        - stop
            -- argument: sensor name
        - shutdown
        '''
        msgraw, address = self.udpsocket.recvfrom(1024)

        #Decode message
        try:
            msg = json.loads(msgraw)
        except:
            logging.warning('Message not valid json, ignoring {}'.format(msgraw))
            # Create an empty msg dict so we will send invalid command response
            msg = {}
            msg['command'] = 'invalid'

        if msg['command'] == 'getdata':
            sensorname = msg['arg']
            data = self.sensors[sensorname].getcurrentdata()
            #Convert to JSON appropriate
            response = {}
            for name, val in data.items():
                if val:
                    dtstr = val[0].strftime('%Y-%m-%d %H:%M')
                    response[name] = (dtstr,val[1])
                else:
                    response[name] = val 
                    
        elif msg['command'] == 'status':
            #Get active sensor names
            sensornames = list(self.sensors.keys())
            response = {'status':'running','sensors':sensornames}
        
        elif msg['command'] == 'getsensor':
            '''
            Return {'measurements':[(measure1,units1),(...)]}
            '''
            sensorname = msg['arg']
            measurelist = []
            for measurename in self.sensors[sensorname].measurements:
                measurelist.append(
                    (measurename,self.sensors[sensorname].units[measurename])
                    )

            response = {'measurements':measurelist}

        elif msg['command'] == 'shutdown':
            self.messages.append(msg['command'])
            response = {'response':'OK'}
        elif msg['command'] == 'stop':
            success = self.stopSensor(msg['arg'])
            if success:
                response = {'response':'OK'}
            else:
                response = {'response':'Sensor not found'}
        elif msg['command'] == 'reload':
            success = self.reload()
            if success:
                response = {'response':'OK'}
            else:
                response = {'response':'Reload failed'}
        else:
            response = {'response':'Invalid Command'}
            
        #Send a response
        self.udpsocket.sendto(json.dumps(response).encode('utf-8'),address)

    def run(self):
        '''
        Run the logger
        Control socket via socket communications
        '''
        #Load configuration
        self.loadconfig()

        #Start listening for UDP
        self.listen = True
        t = threading.Thread(target=self.listenUDP)
        t.start()

        #Create threadpool for concurrent sensor measurement
        self.workerpool = concurrent.futures.ThreadPoolExecutor(
            # use at least 1 worker
            max_workers=max(len(self.sensors),1))

        logging.info('Starting run loop')
        exiting = False
        while not exiting:
            try:
                self.logschedule.run_pending()
                sleeptime = self.logschedule.idle_seconds

                #Check for messages
                if self.messages:
                    msg = self.messages.pop()
                    if msg == 'shutdown':
                        #Shut down threads
                        self.workerpool.shutdown()
                        self.listen=False
                        t.join() #Wait for thread to end
                        print('Shutting down')
                        # Set exiting to break out of the while loop
                        exiting = True
                        # This break only exits the for loop
                        break

                #Sleep for maximum of 1 sec
                if sleeptime > 1: sleeptime = 1
                if sleeptime < 0: sleeptime = 0
                time.sleep(sleeptime)
                
            except KeyboardInterrupt:
                #Shut down threads
                self.workerpool.shutdown()
                self.listen=False
                t.join() #Wait for thread to end
                print('Shutting down')
                break
            except:
                #Handle any other exception so threads
                #don't keep running
                self.workerpool.shutdown()
                self.listen=False
                t.join() #Wait for thread to end
                raise


        #Close database after stopping
        self.db.close()
      
            
def main():
    logger = DataLogger()
    logger.run()

if __name__ == "__main__":
    main()










