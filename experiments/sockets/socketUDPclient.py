'''
Testing a UDP socket server
'''

import socket

HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

try:
    print('Trying to send message')
    sentmsg = sock.sendto(b'Hey how is it going?',(HOST,PORT))

    print('Waiting for response')
    data, server = sock.recvfrom(1024)
    print('Response: {}, Server: {}'.format(data,server))

finally:
    print('Closing socket')
    sock.close()
