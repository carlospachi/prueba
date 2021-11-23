from binance.client import Client
import usuario1 
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from binance import BinanceSocketManager
from binance import *
from binance.client import Client
from binance.enums import *
import websocket
import time
import numpy as np

precio_compra=0

cliente=Client(usuario1.api_key,usuario1.secret_key, tld='com')
moneda="DOGEUSDT"



magin1=cliente.futures_account_balance(symbol=moneda)
print(magin1)
balance=magin1[1]
presupuesto=balance['balance']
inversion=balance['withdrawAvailable']
print(presupuesto)
print(inversion)


























