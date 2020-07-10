'''
Test 3 sensors on PC
A test of three different sensors to gage general functionality
- Dyacon TPH
- RMYoung 61302V
- simSensor

'''

#----- Import databear components ----
from databear.sensors import rmyng61302V, dyaconTPH1,simSensor
from databear import logger,sensorfactory 

#-----  Register custom sensors with the sensor factory ----
#import <module containing custom sensor class>
sensorfactory.factory.register_sensor('rmyBP',rmyng61302V.rmyoungBP)
sensorfactory.factory.register_sensor('dyTPH',dyaconTPH1.dyaconTPH)
sensorfactory.factory.register_sensor('sim',simSensor.sensorSim)

#------ Create a logger ------
config = 'test3sensors.yaml'
datalogger = logger.DataLogger(config)

#------- Run databear ------
#  ctrl-c to stop
datalogger.run()