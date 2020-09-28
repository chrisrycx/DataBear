#!/bin/env python
'''
DataBear command line utility

Use:
databear <cmd> <option>

Commands:
run <config.yaml>
shutdown
other... WIP

'''
import socket
import json
import sys
from databear import logger, databearDB
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
def runDataBear(yamlfile=None):
    '''
    Run databear with optional yaml configuration
    file
    '''
    #Parse YAML file
    if yamlfile:
        config = parseYAML(yamlfile)

        #Connect to database
        db = databearDB.DataBearDB()

        #Load configuration
        db.addSensor()
        db.setSensorConfig()
        db.setLoggingConfig()

    #Run logger
    # *** subprocess ***
    dblogger = logger.DataLogger()
    dblogger.loadconfig()
    dblogger.run()

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
    with open(yamlfile,'rt') as yin:
        configyaml = yin.read()

    config = yaml.safe_load(configyaml)

    return config


