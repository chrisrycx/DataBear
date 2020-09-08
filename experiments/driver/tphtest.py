'''
A basic test of the sensor simulator

'''

#----- Import databear components ----
from databear.sensors import dyaconTPH1old
from databear import logger,sensorfactory 

#-----  Register custom sensors with the sensor factory ----
#import <module containing custom sensor class>
sensorfactory.factory.register_sensor('dyTPH1old',dyaconTPH1old.dyaconTPH)

#------ Create a logger ------
config = 'tphtest.yaml'
datalogger = logger.DataLogger(config)

#------- Run databear ------
#  ctrl-c to stop
datalogger.run()