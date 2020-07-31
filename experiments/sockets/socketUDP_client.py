'''
A test client for UDP socket
'''
import socket

ipaddress = 'localhost'
udp_port = 62000

msg = 'Can you hear me?'

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.settimeout(5)

#Send and receive message
print('Sending message: {}'.format(msg))
sock.sendto(msg.encode('utf-8'),(ipaddress,udp_port))
response = sock.recv(1024)

print(response)

