'''
A basic test of the sensor simulator

'''

#----- Import databear components ----
from databear.sensors import dyaconDataStream
from databear import logger,sensorfactory 

#-----  Register custom sensors with the sensor factory ----
#import <module containing custom sensor class>
sensorfactory.factory.register_sensor('dyDataStream',dyaconDataStream.dyaconDataStream)

#------ Create a logger ------
config = 'streamspeed.yaml'
datalogger = logger.DataLogger(config)

#------- Run databear ------
#  ctrl-c to stop
datalogger.run()