'''
Developing the get data method
'''
import datetime

dt = datetime.datetime.now()

data = {
    'm1':[(dt,1),(dt,2),(dt,3)],
    'm2':[(dt,4),(dt,5),(dt,6)],
    'm3':[(dt,7)],
    'm4':[],
    }

def getcurrentdata():
    '''
    Return most recent data from sensor
    Output:
        {'name':(dt,val),'name2'...}
    Return an empty tuple if no data
    '''
    currentdata = {}
    for key,val in data.items():
        try:
            currentdata[key]=val[-1]
        except IndexError:
            #Assign none if there is nothing in list
            currentdata[key]=None

    return currentdata

print(getcurrentdata())
