'''
DataBear command line utility

Use:
databear <cmd> <option>

Commands:
run <config.yaml>
shutdown
others under development

'''
import socket
import json
import sys
from databear import logger, databearDB
import sqlite3
import yaml
import subprocess

#Setup socket for communication with databear
ipaddress = 'localhost'
udp_port = 62000
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.settimeout(5)

#------------- Functions --------------
def runDataBear(yamlfile=None):
    '''
    Run databear with optional yaml configuration
    file
    '''
    #Parse YAML file and load to database
    if yamlfile:
        '''
        config = parseYAML(yamlfile)

        #Connect to database
        db = databearDB.DataBearDB()

        #Load all sensors
        sensorclasses = sensortypes
        db.load_sensor(sensor['sensortype'])
        
        #Load configuration
        for sensor in sensors:
            db.addSensor()
            db.setSensorConfig()

        for setting in config['settings']:
        db.setLoggingConfig()
        '''
        pass

    #Check to see if logger is already running
    #If so, shutdown for restart
    statusrsp = sendCommand('status')
    print(statusrsp)
    if statusrsp:
        shtdwnrsp = sendCommand('shutdown')
        print(shtdwnrsp)
    
    #Run logger in the background
    print("Running databear with " + sys.executable + " databear/logger.py")
    subprocess.Popen([sys.executable, './databear/logger.py'],
                     cwd="./",
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)

def updateAvailableSensors():
    '''
    Return a list of available sensor classes from
    databear.sensors
    '''

def sendCommand(command,argument=None):
    '''
    Send a command to DataBear
    '''
    msg = {'command':command}
    if argument: msg['arg'] = argument

    #Send and receive message
    print('Sending message: {}'.format(msg))

    try:
        sock.sendto(json.dumps(msg).encode('utf-8'),(ipaddress,udp_port))
        response = sock.recv(1024)
    except:
        response = None

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


#---------------  Main ----------------
def main_cli():
    '''
    Entry point for command line execution
    '''
    #Read in command line args
    if len(sys.argv) < 2:
            print('Arguments: <cmd> <options>')
            return

    cmd = sys.argv[1]
    if len(sys.argv) > 2:
        option = sys.argv[2]
    else:
        option = ''

    if cmd=='run':
        runDataBear()
    else:
        rsp = sendCommand(cmd)
        print(rsp)

if __name__ == "__main__":
    main_cli()
