'''
DataBear Exceptions
'''

class MeasureError(Exception):
    '''
    Exception for measurement failures
    This class is designed to store information
    associated with several failed measurements
    '''
    def __init__(self,sensor_name,failures,messages):
        '''
        Inputs
        failures - a list of measurement names that failed
        messages - a dictionary of messages associated with measurement names
        '''
        self.sensor = sensor_name
        self.measurements = failures
        self.messages = messages

class SensorConfigError(Exception):
    pass

class DataLogConfigError(Exception):
    pass


