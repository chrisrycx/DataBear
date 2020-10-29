'''
Test parsing of streaming data from simDataStream
'''

import re

teststrings = [
    'X5:25:1300,target=1200,frames=50,currentloops=100Z\r\n',
    'arget=1000,frames=50,currentloops=200Z\r\n',
    'X5:30:500,target=500,fra'
]

#Target: 'X{}:{}:{},target={},frames={},currentloops={}Z\r\n'
time_re = re.compile(r'X(\d+):(\d+):(\d+),')
target_re = re.compile(r'target=(\d+),')
loops_re = re.compile(r'currentloops=(\d+)Z')

for tstring in teststrings:
    timeparse = re.findall(time_re,tstring)
    targetparse = re.findall(target_re,tstring)
    loopsparse = re.findall(loops_re,tstring)

    #Print out results
    print('Test string: {}'.format(tstring))

    if timeparse:
        print('Minute: {}'.format(timeparse[0][0]))
        print('Second: {}'.format(timeparse[0][1]))
        print('ms: {}'.format(timeparse[0][2]))
    
    if targetparse:
        print('Target: {}'.format(targetparse[0]))

    if loopsparse:
        print('Loops: {}'.format(loopsparse[0]))






   
        
    
                
               
   

    
