from event import EventHandler
from queue import Queue
import numpy as np 
class MarketHandler(EventHandler):
    """
    This class is meant to do analysis on the incoming market events.
    
    """
    def __init__(self):
        super(MarketHandler,self).__init__()
        self.orderbook_queue = Queue()
        self.central_queue = None

    def eventhandler(self,event):
        price_a = (event.orderbook['A']['bid']+event.orderbook['A']['ask']) / 2
        price_b = (event.orderbook['B']['bid']+event.orderbook['B']['ask']) / 2

        if np.abs(price_a - price_b -1)>3:
            print('Yield signal')
