import numpy as np
import matplotlib.pyplot as plt 
from event import MarketEvent
from datagenerator import MarketGenerator
import pandas as pd



if __name__ == "__main__":
    mg = MarketGenerator()
    pa = []
    pb = []
    diff = []
    for p in mg:
        pa.append(p.orderbook['A']['ask'])
        pb.append(p.orderbook['B']['ask'])
        diff.append(p.orderbook['B']['ask']-p.orderbook['A']['ask'])

     
    df = pd.DataFrame(list(zip(pa,pb)),columns=["pa","pb"])
    df['diff'] = df["pa"]-df["pb"]
    df['mean'] = df['diff'].rolling(13).mean()
    df['std'] = df['diff'].rolling(13).std()

#     plt.plot(df["diff"]) 
#     plt.plot(df["mean"]) 
#     plt.plot(df["std"]) 

    plt.hist(df["mean"],bins=20)
    plt.hist(df["std"],bins=20)


    plt.show()
    
