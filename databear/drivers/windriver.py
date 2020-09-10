'''
A windows driver for databear
'''

class dbdriver:
    def __init__(self):
        '''
        Create a new windows driver instance
        '''
        #Map DataBear ports to Windows
        self.ports = {
            'port1':'COM23'
        }

    def connect(self,databearport):
        '''
        Hardware configuration:
        Windows driver currently requires no
        hardware configuration, so just return
        port name
        '''
        return self.ports[databearport]