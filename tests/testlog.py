'''

This is an example script for using DataBear.
Use this script as a template for your particular implementation.

'''

#----- Import databear components ----
from databear.sensors import dyaconTPH1
from databear import logger,sensorfactory 

#-----  Register custom sensors with the sensor factory ----
#import <module containing custom sensor class>
sensorfactory.factory.register_sensor('dyaconTPH1',dyaconTPH1.dyaconTPH)

#Example
#import mysensor
#sensorfactory.factory.register_sensor('newSensor',mysensor.newSensor)

#------ Create a logger ------
config = 'testlog.yaml'
datalogger = logger.DataLogger(config)

#------- Run databear ------
#  ctrl-c to stop
datalogger.run()