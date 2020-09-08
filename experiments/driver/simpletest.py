'''
Try to create a simplified vision of a system
'''
import minimalmodbus as mm

class windriver:
    '''
    Setup - Windows, RS485 to USB plugged in
    '''
    
    def __init__(self,):
        self.ports = {1:'COM6'}
        '''
        self.port1 = {
            'name':'Port 1',
            'osname':'COM5'
            'type':'modbus',
            'electrical':'RS485'
            'baud':19200
        }
        '''

    def connect(self,portnum,porttype):
        return self.ports[portnum]

driver = windriver()

class modbusPort:
    '''
    Define different types of ports
    
    def __init__(self,portnum,kind)
    '''
    pass

class streamPort:
    pass


class modbusSensor:
    '''
    Basic modbus sensor
    '''
    def __init__(self,portnum,address):
        #Use driver to connect sensor to port
        portname = driver.connect(portnum,porttype='modbus')

        #self.comm = modbusPort(portnum,address)
        #Setup measurement
        self.comm = mm.Instrument(portname,address)
        self.comm.serial.timeout = 0.3
    
    def measure(self):
        '''
        Take a measurement
        '''
        val = self.comm.read_register(201,signed=True)
        val = val/10

        #Output results for testing
        print('Measure =  {}'.format(val))





