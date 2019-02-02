import datetime
import os 
import pandas as pd
import pandas.io.sql as psql
import mysql.connector

from abc import ABCMeta, abstractmethod

from backtest.Event.event import MarketEvent



class DataHandler(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_latest_bars(self, symbol, N=1):
        """
        Returns the last N bars from the latest_symbol list,
        or fewer if less bars are available.
        """
        raise NotImplementedError("Should implement get_latest_bars()")

    @abstractmethod
    def update_bars(self):
        """
        Pushes the latest bar to the latest symbol structure
        for all symbols in the symbol list.
        """
        raise NotImplementedError("Should implement update_bars()")



class SQLDataHandler(DataHandler):
    def __init__(self, db, conn):
        self.db = db
        self.conn = conn

    def get_data(self):

        sql= """
        SELECT daily_price.symbol_id, daily_price.price_date, daily_price.adj_close_price
        FROM securities_master.daily_price
        WHERE symbol_id=(
        SELECT id FROM securities_master.symbol
        WHERE ticker = "CL" )
        ORDER BY daily_price.price_date ASC;
        """
        print(self.db['host'])

        # Create a pandas dataframe from the SQL query
        df = pd.read_sql_query(sql, con=self.conn, index_col='price_date')    
        print(df.head())




if __name__ == "__main__":
    db = { 
    'host':'localhost',
    'user':'sec_user',
    'pass':'password',
    'name':'securities_master'}

    conn = mysql.connector.connect(host=db['host'], 
                                   user=db['user'], 
                                   passwd=db['pass'], 
                                   db=db['name'])
    H = SQLDataHandler(db,conn) 
    H.get_data()
