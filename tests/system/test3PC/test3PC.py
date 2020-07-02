'''
Test 3 sensors on PC
A test of three different sensors to gage general functionality
- Dyacon TPH X 2
- RMYoung 61302V

'''

#----- Import databear components ----
from databear.sensors import rmyng61302V, dyaconTPH1
from databear import logger,sensorfactory 

#-----  Register custom sensors with the sensor factory ----
#import <module containing custom sensor class>
sensorfactory.factory.register_sensor('rmyBP',rmyng61302V.rmyoungBP)
sensorfactory.factory.register_sensor('dyTPH',dyaconTPH1.dyaconTPH)

#------ Create a logger ------
config = 'test3PC.yaml'
datalogger = logger.DataLogger(config)

#------- Run databear ------
#  ctrl-c to stop
datalogger.run()