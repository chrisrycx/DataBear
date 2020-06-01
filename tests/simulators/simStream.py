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
mode = 'timestamp' #Clock or sleep or hybrid or timestamp algorithms
hz = 100  #Output frequency in hz
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
            delta = dt - startdt

            if delta >= interval:
                #Extract datetime information
                minute = dt.minute
                second = dt.second
                ms = dt.microsecond
                deltams = delta/datetime.timedelta(microseconds=1)

                if second != lastsec:
                    print('Loops = {}'.format(loops))
                    loops = 0
                    dataframes = 0

                dataframes = dataframes + 1

                print('{}:{}:{},delta={},frames={}'.format(
                    minute,second,ms,deltams,dataframes),file=f)
                
                startdt = dt
                lastsec = second

            loops = loops + 1

        except KeyboardInterrupt:
            break

#Algorithm "clock"
if mode=='sleep':
    #Set up sleep time
    sleeptime = 1/hz
    
    loops = 0
    dataframes = 0
    lastdt = datetime.datetime.now()
    lastsec = 0

    #Output loop
    while True:
        try:
            #Get datetime
            dt = datetime.datetime.now()
            delta = dt - lastdt
            
            #Extract datetime information
            minute = dt.minute
            second = dt.second
            ms = dt.microsecond
            deltams = delta/datetime.timedelta(microseconds=1)

            if second != lastsec:
                print('Loops = {}'.format(loops))
                loops = 0
                dataframes = 0

            dataframes = dataframes + 1

            print('{}:{}:{},delta={},frames={}'.format(
                minute,second,ms,deltams,dataframes),file=f)
                
            lastdt = dt
            lastsec = second

            loops = loops + 1

            time.sleep(sleeptime)

        except KeyboardInterrupt:
            break

#Algorithm "hybrid"
if mode=='hybrid':
    #Set up sleep time to be a fraction of interval
    sleeptime = (1/hz)*0.75
    
    #Set up clock check
    lastdt = datetime.datetime.now()
    interval = datetime.timedelta(seconds=1/hz) #Seconds between running
    
    loops = 0
    dataframes = 0
    lastsec = 0
    #Output loop
    while True:
        try:
            #Get datetime
            dt = datetime.datetime.now()
            delta = dt - lastdt

            if delta >= interval:
                #Extract datetime information
                minute = dt.minute
                second = dt.second
                ms = dt.microsecond
                deltams = delta/datetime.timedelta(microseconds=1)

                if second != lastsec:
                    print('Loops = {}'.format(loops))
                    loops = 0
                    dataframes = 0

                dataframes = dataframes + 1

                print('{}:{}:{},delta={},frames={}'.format(
                    minute,second,ms,deltams,dataframes),file=f)
                
                lastdt = dt
                lastsec = second
                time.sleep(sleeptime)
                
            loops = loops + 1

        except KeyboardInterrupt:
            break

#Algorithm "timestamp"
#Printing should happen at a fixed schedule rather than based on interval
if mode=='timestamp':
    #Set up sleep time to be a fraction of interval
    #sleeptime = (1/hz)*0.9
    
    #Set up clock check. Start at zero ms into second.
    startdt = datetime.datetime.now()
    startdt = startdt.replace(microsecond=0)
    print('start time: {}'.format(startdt))
    interval = datetime.timedelta(seconds=1/hz) #Seconds between running
    nextdt = startdt + interval
    
    loops = 0
    dataframes = 0
    lastsec = 0
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
                #deltams = delta/datetime.timedelta(microseconds=1)

                if second != lastsec:
                    print('Loops = {}'.format(loops))
                    loops = 0
                    dataframes = 0

                dataframes = dataframes + 1

                print('{}:{}:{},target={},frames={}'.format(
                    minute,second,ms,targetms,dataframes),file=f)
                
                nextdt = nextdt + interval
                lastsec = second
            
            if loops == 0:
                #time.sleep(sleeptime)
                pass
                
            loops = loops + 1

        except KeyboardInterrupt:
            break

f.close()

    



