'''
Testing a streaming sensor input
'''

from databear import logger
from databear import sensorfactory
from databear.sensors import simStream

sensorfactory.factory.register_sensor('simStream', simStream.SimStream)

datalogger = logger.DataLogger('testStream')

#Sensor settings
settings = {
    'serialnumber':555,
    'port':'COM7',
    'baud':19200,
    'hz': 2
}

datalogger.addSensor('simStream','myStream',settings)

datalogger.scheduleMeasurement('myStream',2)
datalogger.scheduleStorage('x','myStream',30)
datalogger.scheduleStorage('y','myStream',20)

datalogger.run()

