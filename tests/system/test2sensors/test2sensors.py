'''
Test 2 sensors on PC
A watered down version of "Test 3 Sensors" due to not having
access to the RMYoung sensor. Use for release testing.
Sensors:
- Dyacon TPH
- simSensor

'''

#----- Import databear components ----
from databear.sensors import dyaconTPH1old,simSensor
from databear import logger,sensorfactory 

#-----  Register custom sensors with the sensor factory ----
#import <module containing custom sensor class>
sensorfactory.factory.register_sensor('dyTPH',dyaconTPH1old.dyaconTPH)
sensorfactory.factory.register_sensor('sim',simSensor.sensorSim)

#------ Create a logger ------
config = 'test2sensors.yaml'
datalogger = logger.DataLogger(config)

#------- Run databear ------
#  ctrl-c to stop
datalogger.run()