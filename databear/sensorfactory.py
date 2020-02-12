'''
Sensor factory
Generates a sensor object of a specific type.

Sensor objects must have the following interface:
- Attributes
    * name - User defined name of sensor
    * sn - Sensor serial number
    * sensor_type - Unique name identifying type of sensor for factory
    * measurements - A list of specific measurements associated with the sensor
    * data - Dictionary with keys for each measurement. Holds associated data.
- Methods
    * measure - perform measurement(s) and parse into 'data' attribute
    * cleardata - clear data for a particular measurement

'''

class sensorFactory:
    '''
    Outputs sensor objects of different types
    '''
    def __init__(self):
        self.sensortypes = {}

    def register_sensor(self,sensortype,sensorobject):
        self.sensortypes[sensortype] = sensorobject

    def get_sensor(self,sensortype,name,settings):
        #Note: .get method on dictionary will return none if not found
        sensorobject = self.sensortypes.get(sensortype)
        if not sensorobject:
            #Evaluates true if sensorobject is none
            raise ValueError(sensorobject)
        
        return sensorobject(name,settings)

#Create sensor factory and register Dyacon
factory = sensorFactory()








