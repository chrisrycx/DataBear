'''
A streaming sensor simulator
Outputs data to a text file at a given rate

Output dataframe:
<min>:<sec>:<ms>::<count per sec>
'''

#import serial
import time
import datetime

#Run Settings
mode = 'clock' #Clock or sleep algorithms
hz = 500  #Output frequency in hz
outfile = 'simdata.txt'

#Set up comm... wait for later
#comm = serial.Serial('COM10',19200,timeout=0)

#Open output file
f = open(outfile,'w')

#Algorithm "clock"
if mode=='clock':
    #Set up clock check
    startdt = datetime.datetime.now()
    interval = datetime.timedelta(seconds=1/hz) #Seconds between running
    
    loops = 0
    dataframes = 0
    lastsec = 0
    #Output loop
    while True:
        try:
            #Get datetime
            dt = datetime.datetime.now()

            if dt >= (startdt + interval):
                #Extract datetime information
                minute = dt.minute
                second = dt.second
                ms = dt.microsecond

                if second != lastsec:
                    print('Loops = {}'.format(loops))
                    loops = 0
                    dataframes = 0

                dataframes = dataframes + 1

                print('{}:{}:{}::{}'.format(minute,second,ms,dataframes),file=f)
                
                startdt = dt
                lastsec = second

            loops = loops + 1

        except KeyboardInterrupt:
            break

f.close()

    



