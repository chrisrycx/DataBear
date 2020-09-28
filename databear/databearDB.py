'''
DataBear database manager class

 - Components:
    -- Ensure database exists
    -- Store and retrieve configuration
        - Get and set methods for whole configuration and individual values
        - Get and set methods for measurements

** Need more documentation here...

'''

import json
import os
import sqlite3


#-------- Database Initialization and Setup ------
class DataBearDB:
    '''
    The sqlite database for databear
    '''

    def __init__(self):
        '''
        Initialize the database manager
        - Check if databear.db already exists in CWD
            -- Create if needed
        - Create connection to database
        '''
        # Check if database exists
        exists = os.path.isfile('databear.db')

        # Initialize database sqlite connection object
        # This will create the file if it doesn't exist, hence the check first
        self.conn = sqlite3.connect('databear.db')
        self.curs = self.conn.cursor()
        self.path = os.path.dirname(__file__)

        # Only initialize if the database didn't already exist
        if not exists:
            with open(self.path + '/databearDB.sql', 'r') as sql_init_file:
                sql_script = sql_init_file.read()

            self.curs.executescript(sql_script)

    # Configuration getters and setters, Getters will need to be changed to return
    # either a dictionary of the configuration or some other type, skeleton for now
    def getSensor(self, sensorid):
        '''
        Return the given sensor's object as a sensor object (name, serial_number, etc.) or None if id is invalid
        '''
        sensor = {}
        id = (sensorid,)
        self.curs.execute("Select * from sensor where sensor_id = ?", id)
        row = self.curs.fetchone()

        if not row:
            return None

        sensor["name"] = row["name"]
        sensor["serial_number"] = row["serial_number"]
        sensor["address"] = row["address"]
        sensor["virtualport"] = row["virutalport"]
        sensor["measure_interval"] = row["measure_interval"]
        return sensor
        
    def sanitizeSensorValues(self, sensor):
        '''
        Helper to sanitize the values from sensor to use in update and insert sqlite statements
        '''
        values = []
        values[0] = sensor["name"]
        values[1] = sensor["serial_number"]
        values[2] = sensor["address"]
        values[3] = sensor["virtualport"]
        values[4] = sensor["sensor_type"]
        values[5] = sensor["measure_interval"]
        return values

    def setSensor(self, sensorid, sensor):
        '''
        Set a given sensor
        sensorid is the id from the table
        sensor is a dict containing the sensor details
        '''
        values = self.sanitizeSensorValues(sensor)
        values[6] = sensorid

        self.curs.execute("Update sensor set name = ?, serial_number = ?, address = ?, virtualport = ?, sensor_type = ?, measure_interval = ?"
                          " where sensor_id = ?", values)
        # TODO: Check for errors, etc.

    def addSensor(self, sensor):
        '''
        Add a new sensor with the values specified in the sensor dict
        '''
        values = self.sanitizeSensorValues(sensor)
        self.curs.execute("INSERT into sensor set (name, serial_number, address, virtualport, sensor_type, measure_interval) "
                          "values (?, ?, ?, ?, ?, ?)")
        # TODO: Check for errors, etc.

    def getSensorConfig(self, sensor_configid):
        '''
        Return the given sensor's configuration or None if id is invalid
        '''
        #Testing
        sensorconfig = {
            "sensorid": "1"
            "measure_interval": 5
            "status": 1
        }
        return sensor


    def setSensorConfig(self, sersor_configid, sensorid, measure_interval, status):
        # May make status separate if it needs to be able to be enabled/disabled without sending
        # all parameters, etc. but use this for now
        pass

    def getActiveSensorIDs(self):
        '''
        Return list of active sensor IDs
        '''
        #Testing
        return [1]

    def getActiveLoggingIDs(self):
        '''
        Return active logger configuration IDs
        '''
        #Testing
        return [1,2]


    def getLoggingConfig(self, logging_configid):
        # Get a logging configuration by it's id

        #Testing
        settings = {
            'measurement_name':'simsecond',
            'sensor_name':'sim1',
            'storage_interval':10,
            'process':'dump'
        }

        return settings

    def setLoggingConfig(self, logging_configid, measurementid, storage_interal, processid, status):
        # Set a logging configuration by its id and values
        pass

    def getDataForLoggingConfig(self, logging_configid):
        # Get all data for a given logging configuration id
        # May add some date range parameters later if it makes sense to do so
        pass

    def getDataForSensorConfig(self, sensor_configid):
        # Same as above but for a given sensor only
        pass

    def storeData(self, datetime, value, sensor_configid, logging_configid, qc_flag):
        '''
        Store data value in database
        Inputs:
            - datetime [string]
        Returns new rowid
        '''
        storeqry = ('INSERT INTO data '
                    '(dtstamp,value,sensor_configid,logging_configid,qc_flag) '
                    'VALUES (?,?,?,?,?)')
        qryparams = (datetime, value, sensor_configid, logging_configid, qc_flag)

        self.curs.execute(storeqry,qryparams)
        self.conn.commit()

        return self.curs.lastrowid

    def close(self):
        '''
        Close all connections
        '''
        self.curs.close()
        self.conn.close()













