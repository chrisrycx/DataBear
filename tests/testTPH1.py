'''
A script to test Dyacon TPH1 sensor
'''
from databear.sensors import dyaconTPH1
import datetime

#Settings
name = 'test'
settings = {
    'serialnumber':555,
    'port':'COM3',
    'address': 5,
    'measurement': 10
}

#Create some fake data
fdata = [
    (datetime.datetime(2020,3,4,12,29),22.0),
    (datetime.datetime(2020,3,4,12,30),22.1),
    (datetime.datetime(2020,3,4,12,31),22.2),
    (datetime.datetime(2020,3,4,12,32),22.3),
    (datetime.datetime(2020,3,4,12,33),22.4),
    (datetime.datetime(2020,3,4,12,34),22.5),
    (datetime.datetime(2020,3,4,12,35),22.5)
]
dt1 = datetime.datetime(2020,3,4,12,30)
dt2 = datetime.datetime(2020,3,4,12,35)

tph = dyaconTPH1.dyaconTPH(name,settings)
#tph.data['airT'] = fdata
#tph.measure()

#tph.cleardata('airT',dt1,dt2)