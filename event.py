import pickle
import json 
from threading import Thread
from datetime import datetime
from queue import Queue

class Event:
    HEADER_LEN = 4 
    CHUNK_SIZE = 1 
    def encode(self):
        msg = pickle.dumps(self) 
        header = bytes(f"{len(msg):<{self.HEADER_LEN}}",'utf-8')
        return header + msg
    
    @classmethod
    def decode(self,msg):
        return pickle.loads(msg) 

    def __repr__(self):
        return json.dumps(self.__dict__)



class MarketEvent(Event):
    def __init__(self,orderbook):
        self.orderbook = orderbook
        self.symbols = list(orderbook.keys())
        self.type='market'
        self.timestamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

class SignalEvent(Event):
    def __init__(self,symbol, time, signal):
        self.symbol=symbol
        self.time = time 
        self.signal = signal
        self.type='signal'

class MessageEvent(Event):
    def __init__(self,msg):
        self.body = msg
        self.type = 'message' 
    
    def mufunc(self):
        print('asdf')


class OrderEvent(Event):
    """
    Handles the event of sending an Order to an execution system.
    The order contains a symbol (e.g. GOOG), a type (market or limit),
    quantity and a direction.
    """

    def __init__(self, symbol, order_type, quantity, direction):
        """
        Initialises the order type, setting whether it is
        a Market order ('MKT') or Limit order ('LMT'), has
        a quantity (integral) and its direction ('BUY' or
        'SELL').

        Parameters:
        symbol - The instrument to trade.
        order_type - 'MKT' or 'LMT' for Market or Limit.
        quantity - Non-negative integer for quantity.
        direction - 'BUY' or 'SELL' for long or short.
        """
        
        self.type = 'order'
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction

    def print_order(self):
        """
        Outputs the values within the Order.
        """
        print ("Order: Symbol=%s, Type=%s, Quantity=%s, Direction=%s" % \
            (self.symbol, self.order_type, self.quantity, self.direction))


class FillEvent(Event):
    """
    Encapsulates the notion of a Filled Order, as returned
    from a brokerage. Stores the quantity of an instrument
    actually filled and at what price. In addition, stores
    the commission of the trade from the brokerage.
    """

    def __init__(self, timeindex, symbol, exchange, quantity, 
                 direction, fill_cost, commission=None):
        """
        Initialises the FillEvent object. Sets the symbol, exchange,
        quantity, direction, cost of fill and an optional 
        commission.

        If commission is not provided, the Fill object will
        calculate it based on the trade size and Interactive
        Brokers fees.

        Parameters:
        timeindex - The bar-resolution when the order was filled.
        symbol - The instrument which was filled.
        exchange - The exchange where the order was filled.
        quantity - The filled quantity.
        direction - The direction of fill ('BUY' or 'SELL')
        fill_cost - The holdings value in dollars.
        commission - An optional commission sent from IB.
        """
        
        self.type = 'fill'
        self.timeindex = timeindex
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost

        # Calculate commission
        if commission is None:
            self.commission = self.calculate_ib_commission()
        else:
            self.commission = commission

    def calculate_ib_commission(self):
        """
        Calculates the fees of trading based on an Interactive
        Brokers fee structure for API, in USD.

        This does not include exchange or ECN fees.

        Based on "US API Directed Orders":
        https://www.interactivebrokers.com/en/index.php?f=commission&p=stocks2
        """
        full_cost = 1.3
        if self.quantity <= 500:
            full_cost = max(1.3, 0.013 * self.quantity)
        else: # Greater than 500
            full_cost = max(1.3, 0.008 * self.quantity)
        full_cost = min(full_cost, 0.5 / 100.0 * self.quantity * self.fill_cost)
        return full_cost



class test(Event):
    def __init__(self):
        self.a = 11
        self.type = 'test'
    

class EventHandler(Thread):
    def __init__(self):
        super(EventHandler,self).__init__()
        self.central_queue = None
        self.queue = Queue()

    def run(self):
#       print('bla')
        try:
            if self.central_queue is None:
                raise AttributeError('Central queue not added')

            while True:
                while not self.queue.empty():
                    event = self.queue.get()
                    self.eventhandler(event)

                    
        except KeyboardInterrupt:
            pass

    def eventhandler(self,event):
        raise NotImplementedError()



if __name__ == "__main__":
    d = {"a":2}
    print(d.keys())
    e = MessageEvent('helllo')
    print(e.__dict__)
#     s = e.encode()
#     f = MessageEvent.load(s)
#     t = MessageEvent('sadfasdf')
# 
#     s = t.encode()
#     t2 = Event.decode(s)
# 
#     print(t2.type)
#     print(dir(t2))
#     print(t2.__dict__)
# 
# #     
# # 
