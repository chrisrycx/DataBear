'''
A simulator for test Druck DPS sensor class
'''

import serial
import datetime
import time

#Set up serial port
comm = serial.Serial('COM3',19200,timeout=2)
address = '3' #Simulated sensor address - number 1 - 32


#Output loop
while True:
    try:
        #Check input buffer for data
        dbytes = comm.in_waiting

        if dbytes > 0:
            #Read in data
            rawdata = comm.read_until().decode('utf-8') #Reads until \n
            print(rawdata)

            #Parse incoming message - Assume <address>:cmd
            inaddress = rawdata[0]
            cmd = rawdata[2]

            if (inaddress == address) and (cmd == 'G'):
                nowtime = datetime.datetime.now()
                fakepressure = 900 + nowtime.minute + nowtime.second/100
                outbytes = str(fakepressure) + '\r\n'
                time.sleep(0.5)
                comm.write(outbytes.encode('utf-8'))
            else:
                comm.write(b'Invalid command\r\n')

    except KeyboardInterrupt:
        break