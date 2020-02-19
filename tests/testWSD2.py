'''
Test Dyacon WSD2 sensor

Platform - Windows
'''

from databear.sensors import dyaconWSD2
from databear import sensorfactory
from databear import logger

#Sensor settings
wsdsettings = {
    'serialnumber':555,
    'port':'COM7',
    'address':'0',
    'measurement':10
}

#Create sensor object for initial testing
#wsd = dyaconWSD2.dyaconWSD2('test',wsdsettings)

#Test sensor with logger
sensorfactory.factory.register_sensor('dyaconWSD2', dyaconWSD2.dyaconWSD2)

datalogger = logger.DataLogger('testWSD2')
datalogger.addSensor('dyaconWSD2','wsd',wsdsettings)

datalogger.scheduleMeasurement('wsd',1)
datalogger.scheduleStorage('speed','wsd',30)
datalogger.scheduleStorage('direction','wsd',30)

datalogger.run()