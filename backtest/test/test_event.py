import unittest
import backtest.Event.event as E
import datetime as d



class TestEventQueue(unittest.TestCase):
    
    def test_event_queue(self):
        q = E.EventQueue()
        self.assertFalse(q.queue_nonempty)
        q.add_event(5)
        q.add_event(10)
        self.assertTrue(q.queue_nonempty)
        q.add_event(1)
        self.assertListEqual(q.queue,[5,10,1])

    
    def test_MarketEvent(self):
        event =E.MarketEvent()
        self.assertTrue(event.type.isupper())


    def test_SignalEvent(self):
        symbol = "Google"
        datetime = d.datetime.now()
        signal_type = 0
        event = E.SignalEvent(symbol,datetime,signal_type)
        self.assertTrue(event.type.isupper())
    
    
    def test_OrderEvent(self):
        symbol = "Google"
        order_type = "MKT"
        quantity = 5
        direction = "BUY"

        event = E.OrderEvent(symbol, order_type, quantity, direction)
        self.assertTrue(event.type.isupper())
    
    
    def test_FillEvent(self):
        timeindex = 0
        symbol = "Googl"
        exchange = "NYS"
        quantity = 500
        direction = "BUY"
        fill_cost = 10000
        commission = 20

        event = E.FillEvent(timeindex, symbol, exchange, quantity, 
                 direction, fill_cost, commission=None)
        self.assertTrue(event.type.isupper())
    

if __name__ == "__main__":
    unittest.main()



