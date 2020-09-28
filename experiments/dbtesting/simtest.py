'''
A basic test of the sensor simulator

'''

#----- Import databear components ----
from databear.sensors import databearSim
from databear import logger
import os, importlib 

#----- Load a hardware driver -------
drivername = os.environ['DBDRIVER']
driver_module = importlib.import_module(drivername)
driver = driver_module.dbdriver()

#-----  Register custom sensors with the sensor factory ----
#import <module containing custom sensor class>
#sensorfactory.factory.register_sensor('simulator',databearSim.databearSim)

#------ Create a logger ------
datalogger = logger.DataLogger(driver)

#------- Run databear ------
datalogger.loadconfig()
datalogger.run()
