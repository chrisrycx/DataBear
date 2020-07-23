'''
Experimental script for developing sockets
'''

import socket
import threading

HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def talk(conn):
    print('Inside thread!')
    data = conn.recv(1024)
    print('I recieved {} bytes'.format(data))
    conn.send(b'Adios')


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    connects = 0 #Keep track of how many connections
    while connects < 2:
        newconn, addr = s.accept()
        print('Connected by', addr)
        t = threading.Thread(target=talk,args=(newconn,))
        t.start()
        connects = connects + 1
            
