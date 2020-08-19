'''
Testing out selectors and a socket
'''
import socket
import selectors
import threading
import time

sel = selectors.DefaultSelector()

#-------- Main Class -------
class looper:

    def __init__(self):
        '''
        Create socket and start thread
        '''
        self.udpsocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.udpsocket.bind(('localhost',62000))
        self.udpsocket.setblocking(False)
        sel.register(self.udpsocket,selectors.EVENT_READ)

        #A message queue
        self.messages = []

        #Simulate some data in RAM
        self.data = {'m1':[0],'m2':[0]}


    def listenUDP(self):
        while self.listen:
            #Check for UDP comm
            event = sel.select(timeout=0)
            if event:
                self.readUDP()

    def readUDP(self):
        '''
        Read message, respond, add message to list
        '''
        msg, address = self.udpsocket.recvfrom(1024)
        print('Got message from {}: {}'.format(address,msg))

        #Send back data if applicable
        msgstr = msg.decode('utf-8')
        if msgstr == 'm1':
            data = 'm1: '+ str(self.data['m1'][-1])
            self.udpsocket.sendto(data.encode('utf-8'),address)
        elif msgstr == 'm2':
            data = 'm2: '+ str(self.data['m2'][-1])
            self.udpsocket.sendto(data.encode('utf-8'),address)
        else:
            self.messages.append(msgstr)

    def run(self):
        '''
        Run loop doing work and looking for messages
        '''
        self.listen = True
        t = threading.Thread(target=self.listenUDP)
        t.start()

        while True:
            try:
                print('Im working')
                m1 = self.data['m1'][-1]
                m2 = self.data['m2'][-1]
                self.data['m1'].append(m1+1)
                self.data['m2'].append(m2+2)

                #Check messages
                if self.messages:
                    msg = self.messages.pop()
                    print('Popped {} off the stack'.format(msg))

                time.sleep(2)
            except KeyboardInterrupt as ki:
                self.listen=False
                t.join() #Wait for thread to end
                print('Shutting down')
                break
            except:
                self.listen=False
                t.join() #Wait for thread to end
                raise
    

if __name__ == "__main__":
    myloop = looper()
    myloop.run()


