'''
A default or base class hardware driver for DataBear
'''

class dbdriver:
    def __init__(self):
        '''
        Create a new windows driver instance
        '''
        #Map DataBear ports to actual hardware
        #port0 returns nothing as it is for internal or 
        #simulated sensors
        self.ports = {
            'port0':'',
        }

    def connect(self,databearport,hardware_settings):
        '''
        Hardware configuration:
        Windows driver currently requires no
        hardware configuration, so just return
        port name
        '''
        return self.ports[databearport]