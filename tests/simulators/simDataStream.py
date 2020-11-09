'''
Simulates a generic data streaming sensor
Outputs data to a serial port at a given frequency

Can verify functionality with Tera Term

Output dataframe:
X<min>:<sec>:<ms>,targetdiffms=<scheduled microsec>Z

Start up:
python simDataStream.py <com> <output rate in Hz>

Algorithm
- Start at next closest second
- Check clock to see if time to output
- Output if time
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
dataframes = 0
lastsec = 0
nbytes = 0
#Output loop
while True:
    try:
        #Get datetime
        dt = datetime.datetime.now()

        if dt >= nextdt:
            #Extract datetime information
            minute = dt.minute
            second = dt.second
            ms = dt.microsecond

            #Calculate difference between current dt and target dt
            msdiff = int((dt - nextdt)/datetime.timedelta(milliseconds=1))

            dataframes = dataframes + 1

            #Send data
            data = 'X{}:{}:{},targetdiffms={}Z\r\n'.format(
                minute,second,ms,msdiff)

            nbytes = comm.write(data.encode('utf-8'))

            #Reset counters
            loops = 0
            
            nextdt = nextdt + interval
            lastsec = second
            #time.sleep(sleeptime)
            
        loops = loops + 1

    except KeyboardInterrupt:
        break

comm.close()

    



