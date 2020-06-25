'''
A basic test of the sensor simulator

'''

#----- Import databear components ----
from databear.sensors import dyaconDataStream2
from databear import logger,sensorfactory 

#-----  Register custom sensors with the sensor factory ----
#import <module containing custom sensor class>
sensorfactory.factory.register_sensor('datastream2',dyaconDataStream2.dyaconDataStream)

#------ Create a logger ------
config = 'streamtest.yaml'
datalogger = logger.DataLogger(config)

#------- Run databear ------
#  ctrl-c to stop
datalogger.run()