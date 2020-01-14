'''
Test DataBear

** Configuration file not yet a thing
'''
import databear.logger

datalogger = databear.logger.DataLogger('testlogger')

#Define measurement settings
airTsettings = {
    'port':'COM7',
    'address':3,
    'register':210,
    'regtype':'float',
    'timeout':0.1
}
RHsettings = {
    'port':'COM7',
    'address':3,
    'register':212,
    'regtype':'float',
    'timeout':0.1
}
RMYsettings = {
    'port':'COM8',
    'baud':9600,
    'timeout':0,
    'dataRE':r'\d\d\d\d.\d\d'
}

datalogger.addSensor('tph',6131)
datalogger.addSensor('rmy',8888)

datalogger.addMeasurement('airT','modbus','tph',airTsettings)
datalogger.addMeasurement('rh','modbus','tph',RHsettings)
datalogger.addMeasurement('bp','stream','rmy',RMYsettings)

datalogger.scheduleMeasurement('rh','tph',5)
datalogger.scheduleMeasurement('bp','rmy',15)
datalogger.scheduleMeasurement('airT','tph',10)

datalogger.scheduleStorage('airT','tph',30)
datalogger.scheduleStorage('bp','rmy',30)

datalogger.run()
