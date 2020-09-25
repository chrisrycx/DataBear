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
        #Check if database exists
        #  **To Do

        #Initialize database sqlite connection object
        self.conn = sqlite3.connect('databear.db')
        self.curs = self.conn.cursor()

        with open(self.path + '/databearDB.sql', 'r') as sql_init_file:
            sql_script = sql_init_file.read()

        self.dbcursor.executescript(sql_script)

    # Configuration getters and setters, Getters will need to be changed to return
    # either a dictionary of the configuration or some other type, skeleton for now
    def getSensorConfig(self, sensor_configid):
        # Return the given sensor's configuration or None if id is invalid
        pass

    def setSensorConfig(self, sersor_configid, sensorid, measure_interval, status):
        # Make make status separate if it needs to be able to be enabled/disabled without sending
        # all parameters, etc. but use this for now
        pass

    def getLoggingConfig(self, logging_configid):
        # Get a logging configuration by it's id
        pass

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













