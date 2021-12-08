from event import EventHandler
from queue import Queue
from event import SignalEvent

class BuyAndHoldStrategy(EventHandler):
    """
    Simplest strategy, for benchmarking and testing
    
    event - Market event 
    """

    def __init__(self):
        super(BuyAndHoldStrategy,self).__init__()
        self.strategy_queue = Queue()
        self.central_queue = None
        self.bought=[]

    def eventhandler(self, event):
        symbols = event.symbols
        for symbol in symbols:
            if symbol not in self.bought:
                signal = SignalEvent(symbol, 0, "LONG")
                self.central_queue.put(signal)
                self.bought.append(symbol)
                print('Generated Sigal for ', symbol)
    


