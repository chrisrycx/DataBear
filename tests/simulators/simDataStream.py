'''
Simulates a generic data streaming sensor
Outputs data to a serial port at a given frequency

Can verify functionality with Tera Term

Output dataframe:
<min>:<sec>:<ms>,target=<scheduled microsec>,frames=<number of frames in sec>

Algorithm
- Start at next closest second
- Check clock to see if time to output
- Output if time
'''

import serial
import time
import datetime

#Run Settings
hz = 40  #Output frequency in hz
#outfile = 'simdata.txt'

#Set up comm
comm = serial.Serial('COM12',19200,timeout=0)

#Open output file
#f = open(outfile,'w')

#Set up sleep time to be a fraction of interval
#sleeptime = (1/hz)*0.9

#Set up clock check. Start at zero ms into second.
startdt = datetime.datetime.now()
nextdt = startdt.replace(microsecond=0) + datetime.timedelta(seconds=1)
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
            targetms = nextdt.microsecond

            if second != lastsec:
                print('Bytes sent = {}'.format(nbytes))
                dataframes = 0

            dataframes = dataframes + 1

            #Send data
            data = 'X{}:{}:{},target={},frames={},currentloops={}\r\n'.format(
                                minute,second,ms,targetms,dataframes,
                                loops)
            nbytes = comm.write(data.encode('utf-8'))

            #Reset counters
            loops = 0
            
            nextdt = nextdt + interval
            lastsec = second
            #time.sleep(sleeptime)
            
        loops = loops + 1

    except KeyboardInterrupt:
        break

#f.close()
comm.close()

    



