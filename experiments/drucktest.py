'''
Quick druck testing
'''

import serial
import datetime
import time
import re

comm = serial.Serial('COM21',9600,timeout=1)
#Measurement sequence
dt = datetime.datetime.now()

#Send a request for measurement
cmd = '20:G\r'
comm.write(cmd.encode('utf-8'))

#Wait for response
time.sleep(1)
response = comm.read_until().decode('utf-8')

#Parse response - should just be a number
m = re.search(r':(\d+\.\d+)',response)

pressure = m.group(0)

print(pressure)

