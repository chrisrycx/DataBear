'''
A basic test of the Druck DPS 8000

'''

#----- Import databear components ----
import druckDPS8000
from databear import logger,sensorfactory 

#-----  Register custom sensors with the sensor factory ----
#import <module containing custom sensor class>
sensorfactory.factory.register_sensor('druck',druckDPS8000.dps8000)

#------ Create a logger ------
config = 'dpstest.yaml'
datalogger = logger.DataLogger(config)

#------- Run databear ------
#  ctrl-c to stop
datalogger.run()