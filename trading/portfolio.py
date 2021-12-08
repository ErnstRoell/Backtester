import numpy as np
import pandas as pd
from queue import Queue

from event import EventHandler
from abc import ABCMeta, abstractmethod
from math import floor

from event import FillEvent, OrderEvent, MarketEvent, SignalEvent

from threading import Thread
from datetime import datetime


class NaivePortfolio(EventHandler):
    """
    Simplest strategy, for benchmarking and testing
    
    event - Market event 
    """

    def __init__(self, symbols, initial_capital=1000):
        super(NaivePortfolio,self).__init__()
        self.portfolio_queue = Queue()
        self.central_queue = None


        self.symbol_list = symbols
        self.prices = {}
        self.start_date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.initial_capital = initial_capital
        
        self.all_positions = self.construct_all_positions()
        self.current_positions = dict( (k,v) for k, v in [(s, 0) for s in self.symbol_list] )

        self.all_holdings = self.construct_all_holdings()
        self.current_holdings = self.construct_current_holdings()



    def eventhandler(self, event):
        if event.type == "signal":
            self.generate_naive_order(event)
        elif event.type == "fill":
            self.update_fill(event)
        elif event.type == "market":
            self.update_prices(event)
            self.update_timeindex(event)
#             self.create_equity_curve_dataframe()




    def update_prices(self, event):
        prices = {}
        for s in event.symbols:
            self.prices[s] = (event.orderbook[s]['bid']+event.orderbook[s]['ask']) / 2

        

    def construct_all_positions(self):
        """
        Constructs the positions list using the start_date
        to determine when the time index will begin.
        """
        d = dict( (k,v) for k, v in [(s, 0) for s in self.symbol_list] )
        d['datetime'] = self.start_date
        return [d]

    def construct_all_holdings(self):
        """
        Constructs the holdings list using the start_date
        to determine when the time index will begin.
        """
        d = dict( (k,v) for k, v in [(s, 0.0) for s in self.symbol_list] )
        d['datetime'] = self.start_date
        d['cash'] = self.initial_capital
        d['commission'] = 0.0
        d['total'] = self.initial_capital
        return [d]

    def construct_current_holdings(self):
        """
        This constructs the dictionary which will hold the instantaneous
        value of the portfolio across all symbols.
        """
        d = dict( (k,v) for k, v in [(s, 0.0) for s in self.symbol_list] )
        d['cash'] = self.initial_capital
        d['commission'] = 0.0
        d['total'] = self.initial_capital
        return d


    def update_timeindex(self, event):
        """
        Adds a new record to the positions matrix for the current 
        market data bar. This reflects the PREVIOUS bar, i.e. all
        current market data at this stage is known (OLHCVI).

        Makes use of a MarketEvent from the events queue.
        """

        # Update positions
        dp = dict( (k,v) for k, v in [(s, 0) for s in self.symbol_list] )
        dp['datetime'] = event.timestamp

        for s in self.symbol_list:
            dp[s] = self.current_positions[s]

        # Append the current positions
        self.all_positions.append(dp)

        # Update holdings
        dh = dict( (k,v) for k, v in [(s, 0) for s in self.symbol_list] )
        dh['datetime'] = event.timestamp
        dh['cash'] = self.current_holdings['cash']
        dh['commission'] = self.current_holdings['commission']
        dh['total'] = self.current_holdings['cash']

        for s in self.symbol_list:
            # Approximation to the real value
            market_value = self.current_positions[s] * self.prices[s]
            dh[s] = market_value
            dh['total'] += market_value

        # Append the current holdings
        self.all_holdings.append(dh)


    def update_positions_from_fill(self, fill):
        """
        Takes a FilltEvent object and updates the position matrix
        to reflect the new position.

        Parameters:
        fill - The FillEvent object to update the positions with.
        """
        # Check whether the fill is a buy or sell
        fill_dir = 0
        if fill.direction == 'BUY':
            fill_dir = 1
        if fill.direction == 'SELL':
            fill_dir = -1

        # Update positions list with new quantities
        self.current_positions[fill.symbol] += fill_dir*fill.quantity

    def update_holdings_from_fill(self, fill):
        """
        Takes a FillEvent object and updates the holdings matrix
        to reflect the holdings value.

        Parameters:
        fill - The FillEvent object to update the holdings with.
        """
        # Check whether the fill is a buy or sell
        fill_dir = 0
        if fill.direction == 'BUY':
            fill_dir = 1
        if fill.direction == 'SELL':
            fill_dir = -1

        # Update holdings list with new quantities
        fill_cost = self.prices[fill.symbol]  # Close price
        cost = fill_dir * fill_cost * fill.quantity
        self.current_holdings[fill.symbol] += cost
        self.current_holdings['commission'] += fill.commission
        self.current_holdings['cash'] -= (cost + fill.commission)
        self.current_holdings['total'] -= (cost + fill.commission)

    def update_fill(self, event):
        """
        Updates the portfolio current positions and holdings 
        from a FillEvent.
        """
        self.update_positions_from_fill(event)
        self.update_holdings_from_fill(event)


    def generate_naive_order(self, signal):
        """
        Simply transacts an OrderEvent object as a constant quantity
        sizing of the signal object, without risk management or
        position sizing considerations.

        Parameters:
        signal - The SignalEvent signal information.
        """
        order = None

        symbol = signal.symbol
        direction = signal.signal

        mkt_quantity = 100
        cur_quantity = self.current_positions[symbol]
        order_type = 'MKT'

        if direction == 'LONG' and cur_quantity == 0:
            order = OrderEvent(symbol, order_type, mkt_quantity, 'BUY')
        if direction == 'SHORT' and cur_quantity == 0:
            order = OrderEvent(symbol, order_type, mkt_quantity, 'SELL')   
    
        if direction == 'EXIT' and cur_quantity > 0:
            order = OrderEvent(symbol, order_type, abs(cur_quantity), 'SELL')
        if direction == 'EXIT' and cur_quantity < 0:
            order = OrderEvent(symbol, order_type, abs(cur_quantity), 'BUY')

        self.central_queue.put(order)


    def create_equity_curve_dataframe(self):
        """
        Creates a pandas DataFrame from the all_holdings
        list of dictionaries.
        """
        curve = pd.DataFrame(self.all_holdings)
        curve.set_index('datetime', inplace=True)
        curve['returns'] = curve['total'].pct_change()
        curve['equity_curve'] = (1.0+curve['returns']).cumprod()
        self.equity_curve = curve
        curve.to_csv('t.csv')
        


if __name__ == "__main__":
    p = NaivePortfolio(["A"])
    orderbook ={'A':{'bid':1,'ask':1,'bid_vol':10,'ask_vol':10}}
    me = MarketEvent(orderbook)
    p.eventhandler(me)
#     fe = FillEvent(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),'A',"x",100,"BUY",10)
#     p.eventhandler(fe)
# 
#     for i in range(200): 
#         orderbook ={'A':{'bid':i,'ask':i,'bid_vol':10,'ask_vol':10}}
#         print(p.prices)
#         me = MarketEvent(orderbook)
#         p.eventhandler(me)
#     
#     for i in range(200,100,-1): 
#         orderbook ={'A':{'bid':i,'ask':i,'bid_vol':10,'ask_vol':10}}
#         print(p.prices)
#         me = MarketEvent(orderbook)
#         p.eventhandler(me)
# 
#     print(p.equity_curve['total'])
#     print(p.equity_curve['equity_curve']) 
# 
