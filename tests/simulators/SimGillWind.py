'''
A Gill Windmaster simulator:
Outputs data at a given frequency following the Gill Windmaster Message
scheme.
'''

import serial
import time
import datetime

#Settings
mode = 'debug' #Normal or debug - debug prints messages
hz = 10  #Output frequency in hz
node = 'Q'  #Node of the virtual wind sensor

#Set up comm
#comm = serial.Serial('COM10',19200,timeout=0)

#Parameters
t = 0  #Psuedo time
x = 0
y = 0
z = 0

#Output loop
while True:
    try:
        #Calculate parameters
        x = 0.25*t
        y = 0.1*t
        z = 0.5*t

        #Create output string
        outstr = 'Q,{:4.2f},{:4.2f},{:4.2f},Z'.format(x,y,z)
        print(datetime.datetime.now().strftime('%M:%S:%f'),outstr)

        #Output to port
        #comm.write(outstr.encode('utf-8'))

        #Increment time
        t=t+1

        #Delay
        time.sleep(1/hz)


    except KeyboardInterrupt:
        break

#Close
#comm.close()