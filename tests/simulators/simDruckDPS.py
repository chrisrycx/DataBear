'''
A simulator for test Druck DPS sensor class
'''

import serial
import time

#Set up serial port
comm = serial.Serial('COM5',19200,timeout=0)


#Output loop
while True:
    try:
        #Check input buffer for data
        dbytes = comm.in_waiting

        if dbytes > 0:
            #Read in data
            rawdata = comm.read_until().decode('utf-8') #Reads until \n
            print(rawdata)

            #Sleep to mimick sensor measurement
            time.sleep(0.5)

            #Respond
            obytes = comm.write(b'Hello!')

    except KeyboardInterrupt:
        break
