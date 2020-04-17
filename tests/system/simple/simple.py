'''

This is a simple test of the databear system on Windows
using DyaconTPH sensor

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
config = 'simple.yaml'
datalogger = logger.DataLogger(config)

#------- Run databear ------
#  ctrl-c to stop
datalogger.run()