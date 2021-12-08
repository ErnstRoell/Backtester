#/bin/bash python3
from serverclient import Client
from threading import Thread
import time
from queue import Queue
import numpy as np
import pandas as pd
import pprint as pp
from event import SignalEvent
from event import EventHandler
from event import FillEvent, OrderEvent
from market import MarketHandler
from strategy import BuyAndHoldStrategy

import datetime
from queue import Queue

from abc import ABCMeta, abstractmethod
from math import floor

from portfolio import NaivePortfolio
"""
TODO Base class EventHandler
"""

class Bot(Client):
    def __init__(self):
        print('Initializing Bot')
        super(Bot, self).__init__()
        # Initialize event Handler
        self.markethandler = MarketHandler()
        self.strategy = BuyAndHoldStrategy()
        self.portfolio = NaivePortfolio(["A","B"])
        
        # Hook up the central queues
        self.markethandler.central_queue = self.central_queue
        self.strategy.central_queue = self.central_queue
        self.portfolio.central_queue = self.central_queue

        # Start the event handlers
        self.markethandler.start()
        self.strategy.start()
        self.portfolio.start()
        

    def run(self):
        try:
            print('EventHandler started listning')
            while True:
                while not self.central_queue.empty():
                    event = self.central_queue.get()
                    print(f'Processing {event.type}')
                    if event.type == 'message':
                        print('Received message')
                    elif event.type == 'market':
#                         self.markethandler.queue.put(event)
                        self.strategy.queue.put(event)
                        self.portfolio.queue.put(event)
                    elif event.type == 'signal':
                        self.portfolio.queue.put(event)
                    elif event.type == 'fill':
                        self.portfolio.queue.put(event)
                    elif event.type == 'order':
                        self.sender_queue.put(event)
                    else:
                        print(f"Error: cant handle for type {event.type}")
        except KeyboardInterrupt:
            pass


            

if __name__ == '__main__':
    bot = Bot()
    bot.start()

