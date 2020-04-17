'''
A script to test Dyacon TPH1 sensor
'''
from databear.sensors import dyaconTPH1
import datetime

#Settings
name1 = 'test1'
settings1 = {
    'serialnumber':555,
    'port':'COM3',
    'address': 4,
    'measurement': 10
}

name2 = 'test2'
settings2 = {
    'serialnumber':666,
    'port':'COM3',
    'address': 5,
    'measurement': 10
}


tph1 = dyaconTPH1.dyaconTPH(name1,settings1)
tph2 = dyaconTPH1.dyaconTPH(name2,settings2)
#tph.data['airT'] = fdata
#tph.measure()

#tph.cleardata('airT',dt1,dt2)