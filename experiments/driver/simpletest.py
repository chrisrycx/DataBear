'''
Testing using a sensor with a driver
'''
from dyaconTPHtest import dyaconTPH
import os

drivername = os.environ['DBDRIVER']
dbdriver = __import__(drivername)


tphsettings = {
    'serialnumber':6036,
    'address':2,
    'port':'port1',
    'measurement':5
}

#Create driver
driver = dbdriver.dbdriver()

#Create sensor
tph = dyaconTPH(
    name='tph',
    sn='555',
    interval=5,
    dbport='port1',
    driver=driver,
    address=2
)

#Test
tph.measure()





   




