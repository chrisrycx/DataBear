'''

This is an example script for using DataBear.
Use this script as a template for your particular implementation.

'''

#----- Import databear components ----
#from databear.sensors import <any predefined sensor classes needed>
from databear import logger,sensorfactory 

#-----  Register custom sensors with the sensor factory ----
#import <module containing custom sensor class>
#sensorfactory.factory.register_sensor(<name for class>,<class>)

#Example
#import mysensor
#sensorfactory.factory.register_sensor('newSensor',mysensor.newSensor)

#------ Create a logger ------
config = 'path to .yaml config file'
datalogger = logger.DataLogger(config)

#------- Run databear ------
#  ctrl-c to stop
datalogger.run()