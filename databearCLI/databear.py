'''
Eventual DataBear Command Line Utility...

Use:
python databear.py <cmd> <option>

'''
import socket
import json
import sys
import databear
import sqlite3
import yaml
import subprocess

#Read in command line args
if len(sys.argv) < 2:
        print('Arguments: <cmd> <options>')
        exit(0)

cmd = sys.argv[1]
if len(sys.argv) > 2:
    option = sys.argv[2]
else:
    option = ''

#------------- Functions --------------
def runDataBear():
    '''
    Check if instance of DataBear exists
    If not start...
    '''
    pass

def sendCommand(command,argument):
    '''
    Send a command to DataBear
    '''
    msg = {'command':cmd,'arg':option}

    #Set up connection
    ipaddress = 'localhost'
    udp_port = 62000

    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.settimeout(5)

    #Send and receive message
    print('Sending message: {}'.format(msg))
    sock.sendto(json.dumps(msg).encode('utf-8'),(ipaddress,udp_port))
    response = sock.recv(1024)
    print(response)
    return response

def parseYAML(yamlfile):
    '''
    parse a YAML configuration file and input
    in database
    '''
    with open(config,'rt') as yin:
                configyaml = yin.read()

    config = yaml.safe_load(configyaml)

    datalogger = config['datalogger']
    loggersettings = datalogger['settings']
    sensors = config['sensors']


