'''
Simulates a generic data streaming sensor
Outputs data to a serial port at a given frequency
19200 Baud

Can verify functionality with Tera Term

Output dataframe:
'sendtime=<secs into minute>'

Start up:
python simDataStream.py <com> <output rate in Hz>

'''

import serial
import time
import datetime
import sys

#Load run parameters
if len(sys.argv) < 2:
    print('Arguments: <com> <Hz>')
    exit()

comport = sys.argv[1]
hz = float(sys.argv[2])

#Set up comm
comm = serial.Serial(comport,19200,timeout=0)

#Set up sleep time to be a fraction of interval
#sleeptime = (1/hz)*0.8

#Set up clock check. Start at zero ms into second.
startdt = datetime.datetime.now()
nextdt = startdt.replace(microsecond=0) + datetime.timedelta(seconds=2)
print('start time: {}'.format(nextdt))
interval = datetime.timedelta(seconds=1/hz) #Seconds between running

loops = 0

#Output loop
while True:
    try:
        #Get datetime
        dt = datetime.datetime.now()
        nextdiff = (dt - nextdt)/datetime.timedelta(microseconds=1)

        if nextdiff > 0:
            
            #Send data
            data = 'sendtime={}Z\r\n'.format(
                dt.strftime('%S.%f'))

            nbytes = comm.write(data.encode('utf-8'))
            
            nextdt = nextdt + interval
        else:
            time.sleep(-1*nextdiff/1000000)
            
        loops = loops + 1

    except KeyboardInterrupt:
        break

print('Total loops: {}'.format(loops))
comm.close()

    



