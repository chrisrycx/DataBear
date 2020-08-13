'''
A test client for DataBear UDP socket
- Send a command and get a response

python DBUDPclient.py <cmd> <option>
'''
import socket
import json
import sys

#Read in command line args
if len(sys.argv) < 2:
        print('Arguments: <cmd> <options>')
        exit(0)

cmd = sys.argv[1]
if len(sys.argv) > 2:
    option = sys.argv[2]
else:
    option = ''

msg = {'command':cmd,'option':option}

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

