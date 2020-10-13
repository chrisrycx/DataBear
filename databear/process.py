'''
Experimental code for developing processing 
of measurement data

General Algorithm
1. Store data following process type
2. Clear data associated with storage from memory

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
    if processtype=='Dump':
        output = dump(data)
    elif processtype=='Sample':
        output = sample(data)
    elif processtype=='Average':
        output = average(data,storetime)
    elif processtype=='Max':
        output = datamax(data,storetime)
    elif processtype=='Min':
        output = datamin(data,storetime)
    else:
        raise KeyError(processtype)

    return output
    

def dump(data):
    '''
    Store all data.
    Change timestamps to strings
    '''
    outdata = []
    for value in data:
        dt = value[0]
        outdata.append((dt,value[1]))

    return outdata
                
def sample(data):
    '''
    Retrieve the first value from current data
    Change datetime to string
    '''
    dt = data[0][0]
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
    dt = storetime

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
    dt = storetime

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
    dt = storetime

    return [(dt,dAve)]



   







