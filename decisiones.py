from binance.client import Client
import usuario1 
from binance import ThreadedDepthCacheManager
from binance import BinanceSocketManager
from binance import DepthCacheManager
from binance import *
import time
import numpy as np
from datos_monedas import *


#lista=lista_mercados()


print(BNBEUR.precio_actual)
maximo,media,minimo=BNBEUR.media_ponderada(2)
print(BNBEUR.media_ponderada(1))
print(minimo)

mas_minuto=False

def medir_tiempo(time):
	time_actual=time.time()
	diferencia_tiempo=time_actual-time
	if diferencia>60:
		return mas_minuto=True











