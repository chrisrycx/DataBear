'''
An experimental hardware driver for DataBear

Setup:
- Windows OS
- RS485 to USB adaptor plugged in (COM?)
'''
import minimalmodbus as mm

class win1port:
    '''
    A DataBear driver
    '''
    def __init__(self):
        '''
        Load configuration?
        Configure GPIO?
        '''
        self.port_types = ['RS485']
        self.ports = {'port1':'COM1'}