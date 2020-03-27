'''
MDL-700 Datalogger
Testing Databear 1.2 on MDL using a Dyacon TPH-1
'''

#Import databear components
# Example: from databear.sensors import dyaconTPH1,dyaconWSD2,simStream 
from databear.sensors import dyaconWSD1, maxBotixAlt
from databear import logger, sensorfactory 

#Import MDL functions
import mdl_functions

#Import other libraries
import sys
import yaml

#Register project sensors with sensor factory
#   register_sensor(<sensortype>,<sensorclass>)
#The sensortype string should match the sensortype specified in the yaml
#Example: sensorfactory.factory.register_sensor('simStream', simStream.SimStream)
sensorfactory.factory.register_sensor('dyaconWSD1', dyaconWSD1.dyaconWSD1)
sensorfactory.factory.register_sensor('maxBotixAlt', maxBotixAlt.maxBotixAlt)

#Read in path to YAML from commandline arg
if len(sys.argv) < 2:
        print('Enter path to config file from current directory')
        exit(0)

configpath = sys.argv[1]

#Import config file
with open(configpath,'rt') as yin:
    configyaml = yin.read()

config = yaml.safe_load(configyaml)

#Update configuration for compatibility with databear
config = mdl_functions.configUpdate(config)

#Create a logger
datalogger = logger.DataLogger(config)

#Configure GPIO
for sensor in datalogger.sensors.values():
    #Get serial settings from sensor
    port = sensor.port
    rs = sensor.rs
    duplex = sensor.duplex
    resistors = sensor.resistors
    bias = sensor.bias
    #Configure port
    mdl_functions.gpioconfig(port,rs,duplex,resistors,bias)

#Run logger
datalogger.run()
