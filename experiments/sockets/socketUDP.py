'''
Testing a UDP socket server
'''

import socket
import threading
import time

HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def recvudp(conn):
    print('Inside thread!')
    messages = 0
    while messages < 2:
        data, address = conn.recvfrom(1024)
    
        if data:
            print('I recieved {} bytes from {}'.format(data,address))
            conn.sendto(b'Thanks for that message!')
            messages = messages + 1



with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.bind((HOST, PORT))
    t = threading.Thread(target=recvudp,args=(sock,))
    t.start()
    loops = 0
    while True:
        print('Doing some work! Loops: {}'.format(loops))
        loops = loops + 1
        time.sleep(1)