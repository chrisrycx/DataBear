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
from datetime import timedelta
import concurrent.futures
import threading #For IPC
import selectors #For IPC via UDP
import socket
import json
import time #For sleeping during execution
import csv
import sys #For command line args
import logging

#Testing
from databear.sensors import databearSim


#-------- Logger Initialization and Setup ------
class DataLogger:
    '''
    A data logger
    '''
    #Error logging format
    errorfmt = '%(asctime)s %(levelname)s %(lineno)s %(message)s'

    def __init__(self,dbdriver):
        '''
        Initialize a new data logger
        Input (various options)
       
        dbdriver:
            - An instance of a DB hardware driver
        '''
        #Initialize attributes
        self.sensors = {}
        self.loggersettings = [] #Form (<measurement>,<sensor>)
        self.logschedule = schedule.Scheduler()
        self.driver = dbdriver
        self.db = DataBearDB()

        #Configure UDP socket for API
        self.udpsocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.udpsocket.bind(('localhost',62000))
        self.udpsocket.setblocking(False)
        self.sel = selectors.DefaultSelector()
        self.sel.register(self.udpsocket,selectors.EVENT_READ)
        self.listen = False
        self.messages = []
        self.db = databearDB.DataBearDB(config)

        #Set up error logging
        logging.basicConfig(
                format=DataLogger.errorfmt,
                filename='databear_error.log')

    def loadconfig(self):
        '''
        Get configuration out of database and
        start sensors
        '''
        #Get list of active sensors and logging
        sensorids = self.db.getActiveSensorIDs()
        loggingconfigs = self.db.getActiveLoggingIDs()
        
        #Register sensor... not sure where to do this...
        sensorfactory.factory.register_sensor('dbSim',databearSim.databearSim)
        
        #Configure logger
        for sensorid in sensorids:
            sensorsettings = self.db.getSensorConfig(sensorid)

            self.addSensor(
                sensorsettings['name'],
                sensorsettings['serial_number'],
                sensorsettings['address'],
                sensorsettings['virtualport'],
                sensorsettings['sensortype']
                )
            self.scheduleMeasurement(
                sensorsettings['sensor_configid'],
                sensorsettings['name'],
                sensorsettings['measure_interval']
                )

        for loggingid in loggingconfigs:
            storagesetting = self.db.setLoggingConfig(loggingid)
                
            self.scheduleStorage(
                setting['measurement_name'],
                setting['sensor_name'],
                setting['storage_interval'],
                setting['process'])
               
      
    def addSensor(self,sensortype,name,settings):
        '''
        Add a sensor to the logger
        '''
        #Create sensor object
        sensor = sensorfactory.factory.get_sensor(
            sensortype,
            name,
            settings['serialnumber'],
            settings['address'],
            settings['measure_interval']
            )

        #"Connect" virtual port to hardware using driver
        #Ignore if port0 (simulated sensors)
        if settings['virtualport']!='port0':
            hardware_port = self.driver.connect(
                settings['virtualport'],sensor.hardware_settings)
        else:
            hardware_port = ''

        #"Connect" sensor to hardware
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
    
    def scheduleMeasurement(self,sensorname,interval):
        '''
        Schedule a measurement
        Interval is seconds
        '''
        #Check interval to ensure it isn't too small
        if interval < self.sensors[sensorname].min_interval:
            raise DataLogConfigError('Logger frequency exceeds sensor max')
        
        #Schedule measurement
        m = self.doMeasurement
        self.logschedule.every(interval).do(m,sensorname)
    
    def doMeasurement(self,sensorname,storetime,lasttime):
        '''
        Perform a measurement on a sensor
        Inputs
        - Sensor name
        - storetime and lasttime are not currently used here
          but are passed by Schedule when this function is called.
        '''
        mfuture = self.workerpool.submit(self.sensors[sensorname].measure)
        mfuture.sname = sensorname
        mfuture.add_done_callback(self.endMeasurement)
        
    def endMeasurement(self,mfuture):
        '''
        A callback after measurement is complete
        Use to log any exceptions that occurred
        input: mfuture - a futures object that gets passed when complete
        '''
        print(self.sensors[mfuture.sname])

        #Retrieve exception. Returns none is no exceptions
        merrors = mfuture.exception()

        #Log exceptions
        if merrors:
            for m in merrors.measurements:
                logging.error('{}:{} - {}'.format(
                        merrors.sensor,
                        m,
                        merrors.messages[m]))

    def scheduleStorage(self,name,sensor,interval,process):
        '''
        Schedule when storage takes place
        '''
        #Check storage frequency doesn't exceed measurement frequency
        if interval < self.sensors[sensor].interval:
            raise DataLogConfigError('Storage frequency exceeds sensor measurement frequency')

        s = self.storeMeasurement
        #Note: Some parameters for function supplied by Job class in Schedule
        self.logschedule.every(interval).do(s,name,sensor,process)

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
            
    def listenUDP(self):
        '''
        Listen on UDP socket
        '''
        while self.listen:
            #Check for UDP comm
            event = self.sel.select(timeout=0)
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
        msg = json.loads(msgraw)
        if msg['command'] == 'getdata':
            sensorname = msg['arg']
            data = self.sensors[sensorname].getcurrentdata()
            #Convert to JSON appropriate
            datastr = {}
            for name, val in data.items():
                if val:
                    dtstr = val[0].strftime('%Y-%m-%d %H:%M')
                    datastr[name] = (dtstr,val[1])
                else:
                    datastr[name] = val 
                    
            response = {'response':'OK','data':datastr}
        elif msg['command'] == 'status':
            response = {'response':'OK'}
        elif msg['command'] == 'shutdown':
            self.messages.append(msg['command'])
            response = {'response':'OK'}
        elif msg['command'] == 'stop':
            success = self.stopSensor(msg['arg'])
            if success:
                response = {'response':'OK'}
            else:
                response = {'response':'Sensor not found'}
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
            max_workers=len(self.sensors))

        while True:
            try:
                self.logschedule.run_pending()
                sleeptime = self.logschedule.idle_seconds
                if sleeptime > 0:
                    time.sleep(sleeptime)

                #Check for messages
                if self.messages:
                    msg = self.messages.pop()
                    if msg == 'shutdown':
                        #Shut down threads
                        self.workerpool.shutdown()
                        self.listen=False
                        t.join() #Wait for thread to end
                        print('Shutting down')
                        break
            except AssertionError:
                logging.error('Measurement too late, logger resetting')
                self.logschedule.reset()
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


        #Close CSV after stopping
        self.db.close()
      
            









