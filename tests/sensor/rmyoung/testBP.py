'''
A basic test of the sensor simulator

'''

#----- Import databear components ----
from databear.sensors import rmyng61302V
from databear import logger,sensorfactory 

#-----  Register custom sensors with the sensor factory ----
#import <module containing custom sensor class>
sensorfactory.factory.register_sensor('rmyBP',rmyng61302V.rmyoungBP)

#------ Create a logger ------
config = 'testBP.yaml'
datalogger = logger.DataLogger(config)

#------- Run databear ------
#  ctrl-c to stop
datalogger.run()