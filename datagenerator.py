from event import Event, MarketEvent
import random
import time
from threading import Thread
import numpy as np
import pprint as pp
import matplotlib.pyplot as plt


"""
Data generator class.
Generates OrderBookEvents. 
Yield an update of the stockmarkent to be send to the client.



"""

class DataFeed(Thread):
    def __init__(self):
        super(DataFeed,self).__init__()
        self.central_queue = None
        self.generator = MarketGenerator()

    def run(self):
        for data in self.generator:
            time.sleep(1.5)
            self.central_queue.put(data)



def MarketGenerator():
    price_A = 0 
    price_B = 0 
    max_it = 20
    spread = 0
    alpha, beta = 1,1
    mean = 1
    sigma = 1
    
    for t in range(max_it):
        dPrice_A = np.random.normal(mean,sigma) 
        price_A += dPrice_A

        price_B = alpha*price_A + np.random.normal(0,1) + beta
        orderbook ={'A':{'bid':price_A+spread,'ask':price_A-spread,'bid_vol':10,'ask_vol':10},'B':{'bid':price_B+spread,'ask':price_B-spread,'bid_vol':10,'ask_vol':10}}
        yield MarketEvent(orderbook) 

if __name__ == "__main__":
    mg = MarketGenerator()
    pa = []
    pb = []
    diff = []
    for p in mg:
        pa.append(p.orderbook['A']['ask'])
        pb.append(p.orderbook['B']['ask'])
        diff.append(p.orderbook['B']['ask']-p.orderbook['A']['ask'])

#     plt.plot(pa)
#     plt.plot(pb)
#     plt.plot(diff)

    plt.hist(diff)
    plt.show()
    

