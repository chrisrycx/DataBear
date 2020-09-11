'''
Test 3 sensors on PC
A test of three different sensors to gage general functionality
- Dyacon TPH
- RMYoung 61302V
- simSensor

'''

#----- Import databear components ----
from databear.sensors import rmyng61302V, dyaconTPH1old,simSensor
from databear import logger,sensorfactory
import os, importlib

#----- Load a hardware driver -------
drivername = os.environ['DBDRIVER']
driver_module = importlib.import_module(drivername)
driver = driver_module.dbdriver()

#-----  Register custom sensors with the sensor factory ----
#import <module containing custom sensor class>
sensorfactory.factory.register_sensor('rmyBP',rmyng61302V.rmyoungBP)
sensorfactory.factory.register_sensor('dyTPH',dyaconTPH1old.dyaconTPH)
sensorfactory.factory.register_sensor('sim',simSensor.sensorSim)

#------ Create a logger ------
config = 'test3sensors.yaml'
datalogger = logger.DataLogger(config,driver)

#------- Run databear ------
#  ctrl-c to stop
datalogger.run()