'''
Test functionality of sensor base class
'''
from datetime import datetime
from databear.sensors import sensor

#Test time
testdt1 = datetime(2022,5,4,13,35)
testdt2 = datetime(2022,5,4,12,20)

#Dummy sensor data
testdata = [
    (datetime(2022,5,4,12,0),0),
    (datetime(2022,5,4,12,10),1),
    (datetime(2022,5,4,12,20),2),
    (datetime(2022,5,4,13,30),3),
    (datetime(2022,5,4,13,40),4),
    (datetime(2022,5,4,14,50),5),
    (datetime(2022,5,4,15,30),6)
]

#Instantiate sensor
test_sensor = sensor.Sensor('test',1234,0)

#Set data on sensor
test_sensor.data['m1'] = testdata
test_sensor.data['m2'] = testdata.copy()

#Test clear data
test_sensor.cleardata('m1',testdt1)
test_sensor.cleardata('m2',testdt2)

print(test_sensor.data['m1'])
print(test_sensor.data['m2'])


