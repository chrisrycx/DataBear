'''
DataBear Exceptions
'''

class MeasureError(Exception):
    pass

class SensorConfigError(Exception):
    pass

class DataLogConfigError(Exception):
    pass


#Testing
if __name__ == "__main__":
    x = 1
    y = 2

    if x<y:
        raise MeasureError('This is a test')

    print('hello')