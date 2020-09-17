'''
DataBear database manager class

 - Components:
    -- Ensure database exists
    -- Store and retrieve configuration
        - Get and set methods for whole configuration and individual values
        - Get and set methods for measurements

** Need more documentation here...

'''

import yaml
import json
import sqlite3


#-------- Database Initialization and Setup ------
class DataBearDB:
    '''
    The sqlite database for databear
    '''
    #Error logging format
    errorfmt = '%(asctime)s %(levelname)s %(lineno)s %(message)s'

    def __init__(self,config):
        '''
        Initialize the database manager
        - Ensure database exists and create if needed
        - Import config values from given config into config tables
          if config is given
        '''
        #Initialize database sqlite conneciton object


        #Determine what input is
        if (isinstance(config,dict)) or (config[-4:]=='yaml'):
            #Pass dictionary to loadconfig
            self.loadconfig(config)

    def loadconfig(self,config):
        '''
        Load configuration file
        Input options
        - path to yaml
        - dictionary with configuration

        - In either option inject values into config database tables
        '''

        if isinstance(config,str):
            #Import configuration from yaml
            with open(config,'rt') as yin:
                configyaml = yin.read()

            config = yaml.safe_load(configyaml)

        # Inject data from config into config tables

    def ensureExists(self):
        # Check if the database file exists
        # If it exists create sqlite object and open it

        # If it doesn't exist use database creation script to
        # initialize the database then create sqlite object and open it.
        pass

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

    def getHardwareConfig(self, hardware_configid):
        # Get a hardware configuration by its id
        pass

    def setHardwareConfig(self, hardware_configid, sensorid, comm_type, port, address):
        # Set a hardware configuration by its id and values
        pass

    def getDataForLoggingConfig(self, logging_configid):
        # Get all data for a given logging configuration id
        # May add some date range parameters later if it makes sense to do so
        pass

    def getDataForSensorConfig(self, sensor_configid):
        # Same as above but for a given sensor only
        pass

    def setData(self, datetime, value, sensor_configid, logging_configid, qc_flag):
        # Add data to the database data table
        pass












