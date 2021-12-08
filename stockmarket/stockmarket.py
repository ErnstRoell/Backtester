import time
from queue import Queue
from threading import Thread
from datetime import datetime

import sys

from event import Event, MessageEvent, FillEvent
from serverclient import Server
from datagenerator import DataFeed

class Stockmarket(Server):
    def __init__(self):
        # Here the central_queue is created
        super(Stockmarket,self).__init__()
        self.datafeed = DataFeed()
        self.datafeed.central_queue = self.central_queue
        self.datafeed.start()

    def run(self):
        try:
            print('EventHandler started listning')
            while True:
                while not self.central_queue.empty():
                    event = self.central_queue.get()
                    print(f'Processing message of type {event.type}')
                    if event.type == 'message':
                        print('sending message back')
                        self.sender_queue.put(event)
                    elif event.type == 'market':
#                         print('Sending new data to client')
                        self.sender_queue.put(event)
                    elif event.type == 'order':
                        fill_event = FillEvent(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                                  event.symbol,
                                  "ARCA",
                                  event.quantity,
                                  event.direction, 10, None)
#                     
                        self.sender_queue.put(fill_event)
                    else:
                        print(f"Error: cant handle for type {event.type}")
        except KeyboardInterrupt:
            pass

stockmarket = Stockmarket()
stockmarket.start()

    




