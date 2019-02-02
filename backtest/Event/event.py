class EventQueue:
    #Constructor creates a list
    def __init__(self):
        self.queue = list()
        self.queue_nonempty = False

    #Adding elements to queue
    def add_event(self,data):
        if len(self.queue) >5:
            print("Warning: que getting long")
        self.queue.append(data) 
        self.queue_nonempty = True



    #Removing the last element from the queue
    def get_event(self):
        if len(self.queue) == 1:
            self.queue_nonempty = False
            return self.queue.pop(0)
        elif len(self.queue) >1:
            return self.queue.pop(0)
        elif len(self.queue)==0:
            return ("Queue Empty!")


class Event():
    pass



class MarketEvent(Event):
    def __init__(self):
        self.type = "MARKET"
    

class SignalEvent(Event):
    def __init__(self, symbol,datetime,signal_type):
        self.type = "SIGNAL"
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type


class OrderEvent(Event):
    def __init__(self,symbol,order_type,quantity,direction):
        self.type = "ORDER"
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction
    
    def print_order(self):
        print("Order: Symbol=%s, Type=%s, Quantity=%s, Direction=%s" % \
            (self.symbol, self.order_type, self.quantity, self.direction))



class FillEvent(Event):
    def __init__(self, timeindex,symbol,exchange,quantity,direction,fill_cost,commission = 0):
        self.type = "FILL"
        self.timeindex = timeindex
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost

        # TODO: Has to be expanded to more complex computation
        self.commission = commission

