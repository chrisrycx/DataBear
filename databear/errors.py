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


#Testing
if __name__ == "__main__":
    x = 1
    y = 2

    if x<y:
        msg = {'x':'Testing','y':'Testing'}
        raise MeasureError(['x','y'],msg)

    print('hello')