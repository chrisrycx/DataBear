'''
Turn off databear...testing
'''
import socket
import json

#Set up connection
ipaddress = 'localhost'
udp_port = 62000

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.settimeout(5)

#Send and receive message
msg={'command':'shutdown'}
print('Sending shutdown message')
sock.sendto(json.dumps(msg).encode('utf-8'),(ipaddress,udp_port))
response = sock.recv(1024)
print(response)
