'''
A basic test of the sensor simulator

'''

#----- Import databear components ----
from databear.sensors import rmyng61302V
from databear import logger,sensorfactory
import os, importlib 

#----- Load a hardware driver -------
drivername = os.environ['DBDRIVER']
driver_module = importlib.import_module(drivername)
driver = driver_module.dbdriver() 

#-----  Register custom sensors with the sensor factory ----
#import <module containing custom sensor class>
sensorfactory.factory.register_sensor('rmyBP',rmyng61302V.rmyoungBP)

#------ Create a logger ------
config = 'testBP.yaml'
datalogger = logger.DataLogger(config,driver)

#------- Run databear ------
#  ctrl-c to stop
datalogger.run()