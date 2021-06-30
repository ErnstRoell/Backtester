# Backtester
This project is an event driven backtesting system for backtesting trading strategies using python. 
This program is inspired by the article series on Quantstart, see <https://www.quantstart.com/articles>, where parts of the code can be found. 
The majority of this code is a heavy edited version of the code there. 

The main improvements are that each independent component can work
asynchronously via threading and that the communication with the simulated
stockmarket happens via a server client architecture making use of sockets.  
The original (and heavily modified code) originates from LifeOverflow's tutorial
series on [Pwn Adventures: Pwnie Island](https://www.youtube.com/watch?v=RDZnlcnmPUA&list=PLhixgUqwRTjzzBeFSHXrw9DnQtssdAwgG) and in particular the part on decoding the network
protocol using proxies. 

# Installation
To run the simulation, clone the repo and open two terminals. 
first run stockmarket.py to set up the stockmarket. 
In the other terminal, run bot.py and the simulation should start. 


# Description of the components

## Stockmarket

## Bot




