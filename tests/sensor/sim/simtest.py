'''
A basic test of the sensor simulator

'''

#----- Import databear components ----
from databear.sensors import simulator
from databear import logger,sensorfactory 

#-----  Register custom sensors with the sensor factory ----
#import <module containing custom sensor class>
sensorfactory.factory.register_sensor('sensorSim',simulator.sensorSim)

#------ Create a logger ------
config = 'simtest.yaml'
datalogger = logger.DataLogger(config)

#------- Run databear ------
#  ctrl-c to stop
datalogger.run()