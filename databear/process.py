'''
Experimental code for developing processing 
of measurement data

General Algorithm
1. Store data following process type
2. Clear data associated with storage from memory

Types
- dump: store all data in memory
- sample: store more recent measurement
- average: average all data since last measurement

Assumes
- Measurement scheduled at same time as storage takes place first(?)
'''

from datetime import datetime
import numpy as np


def calculate(processtype,data,storetime):
    '''
    Determines what process function to use
    Inputs:
        - processtype = 'dump','sample','average','max','min'
        - data - list of data to store [(datetime,val),...]
        - storetime - datetime of the storage operation
    Output:
        - list of data to be stored [('YYYY-MM-DD HH:MM',val),...]
    '''
    if processtype=='dump':
        output = dump(data)
    elif processtype=='sample':
        output = sample(data)
    elif processtype=='average':
        output = average(data,storetime)
    elif processtype=='max':
        output = datamax(data,storetime)
    elif processtype=='min':
        output = datamin(data,storetime)
    else:
        print('error')

    return output
    

def dump(data):
    '''
    Store all data.
    Change timestamps to strings
    '''
    outdata = []
    for value in data:
        dt = value[0].strftime('%Y-%m-%d %H:%M:%S')
        outdata.append((dt,value[1]))

    return outdata
                
def sample(data):
    '''
    Retrieve the first value from current data
    Change datetime to string
    '''
    dt = data[0][0].strftime('%Y-%m-%d %H:%M:%S')
    outdata = [(dt,data[0][1])]

    return outdata

def average(data,storetime):
    '''
    Average input data
    Assumes data is evenly spaced
    '''
    #Extract values to list
    vals = [x[1] for x in data]
    datanp = np.array(vals)

    #Average
    dAve = np.average(datanp)

    #Convert storetime to string
    dt = storetime.strftime('%Y-%m-%d %H:%M:%S')

    return [(dt,dAve)]

def datamax(data,storetime):
    '''
    Output max
    '''
    #Extract values to list
    vals = [x[1] for x in data]
    datanp = np.array(vals)

    #Average
    dAve = np.max(datanp)

    #Convert storetime to string
    dt = storetime.strftime('%Y-%m-%d %H:%M:%S')

    return [(dt,dAve)]

def datamin(data,storetime):
    '''
    Output min
    '''
    #Extract values to list
    vals = [x[1] for x in data]
    datanp = np.array(vals)

    #Average
    dAve = np.min(datanp)

    #Convert storetime to string
    dt = storetime.strftime('%Y-%m-%d %H:%M:%S')

    return [(dt,dAve)]


#------------- Testing -------------
if __name__ == "__main__":
    #Test parameters
    simtime = datetime(2020,2,27,12,20)

    testdata = [
        ('2020-02-27 11:00',1),
        ('2020-02-27 11:10',2),
        ('2020-02-27 11:20',3),
        ('2020-02-27 11:30',4),
        ('2020-02-27 11:40',5),
        ('2020-02-27 11:50',6),
        ('2020-02-27 12:00',7),
        ('2020-02-27 12:10',8)
    ]

    #Convert testdata to form (<datetime>,val)
    data = []
    for row in testdata:
        timestr = row[0]
        dt = datetime.strptime(timestr,'%Y-%m-%d %H:%M')
        data.append((dt,row[1]))

    #Test functions
    test1 = calculate('dump',data,simtime)
    test2 = calculate('sample',data,simtime)
    test3 = calculate('average',data,simtime)
    test4 = calculate('max',data,simtime)
    test5 = calculate('min',data,simtime)

    print(test1)
    print(test2)
    print(test3)
    print(test4)
    print(test5)









