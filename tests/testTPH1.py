'''
A script to test Dyacon TPH1 sensor
'''
from databear.sensors import dyaconTPH1
import datetime

#Settings
name = 'test'
settings = {
    'serialnumber':555,
    'port':'COM7',
    'address': 4,
    'measurement': 10
}
dt1 = datetime.datetime(2020,3,4,12,30)
dt2 = datetime.datetime(2020,3,4,12,35)

tph = dyaconTPH1.dyaconTPH(name,settings)