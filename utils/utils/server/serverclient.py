import socket 
import random 
import time
from threading import Thread
from queue import Queue

HEADER_LEN=4
CHUNK_SIZE=1
q = Queue(maxsize=0)


from utils.events.events import Event, MessageEvent

class Server2Client(Thread):
    """
    Responsible for sending data to the client 
    """
    def __init__(self,host,port,name=None):
        super(Server2Client,self).__init__()
        self.name = name
        self.host=host
        self.port=port
        self.server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server.bind((socket.gethostname(),port))
        print(f'The {self.name} is waiting for incoming connections at port {port}')
        self.server.listen(5)
        self.clientsocket, address = self.server.accept()
        self.sender_queue=None
        print(f"Connection from {address} established!")

    def run(self):
        while True:
            try: 
                while not self.sender_queue.empty():
                    message = self.sender_queue.get()
#                     print(f"Sending from queue: {message}")
                    self.clientsocket.send(message.encode())
                    self.sender_queue.task_done()
            except KeyboardInterrupt:
                self.clientsocket.close()


class Client2Server(Thread):
    def __init__(self,host,port,name=None):
        super(Client2Server,self).__init__()
        self.name = name

        print(f'Connecting from {self.name} to port {port}')
        self.central_queue = None
        self.host=host
        self.port=port
        self.serversocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.connect((socket.gethostname(),port))
        print('Connection made!')

    def run(self):
        while True:
            try:
                header = self.serversocket.recv(HEADER_LEN)
                if header:
                    data_len = int(header)
                    full_msg = bytes("",'utf-8')
                    i=0
                    while i < data_len:
                        data = self.serversocket.recv(CHUNK_SIZE)
                        full_msg += data
                        i+=CHUNK_SIZE 
                    
                    e = Event.decode(full_msg)
#                     print(f'Received message:{e}')
                    self.central_queue.put(e)
            except KeyboardInterrupt:
                self.serversocket.close()

class Server(Thread):
    def __init__(self):
        super(Server,self).__init__()
        self.sender_queue = Queue()
        self.central_queue = Queue()
        

        self.s2c=Server2Client(socket.gethostname(),3333,'Server')
        self.s2c.sender_queue=self.sender_queue
        self.s2c.start()
        
        self.c2s=Client2Server(socket.gethostname(),3000,'Server')
        self.c2s.central_queue=self.central_queue
        self.c2s.start()
       
    def run(self):
        while True:
            while not self.central_queue.empty():
                msg = self.central_queue.get()
                self.sender_queue.put(msg)
                self.central_queue.task_done()

            
class Client(Thread):
    def __init__(self):
        super(Client,self).__init__()
        self.sender_queue = Queue()
        self.central_queue = Queue()
        

        self.c2s=Client2Server(socket.gethostname(),3333,'Client')
        self.c2s.central_queue=self.central_queue
        self.c2s.start()

        self.s2c=Server2Client(socket.gethostname(),3000,'Client')
        self.s2c.sender_queue=self.sender_queue
        self.s2c.start()
       
    def run(self):
        while True:
            while not self.central_queue.empty():
                msg = self.central_queue.get()
                self.sender_queue.put(msg)
                self.central_queue.task_done()


if __name__ == "__main__":
    server=Server()
    server.start()
