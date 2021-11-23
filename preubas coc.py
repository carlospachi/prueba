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


cliente=Client(usuario1.api_key,usuario1.secret_key)
try:
	eth_balance = cliente.get_asset_balance(asset='EUR')
	print(eth_balance)
	print("Mi presupuesto de ETH: ",eth_balance["free"])
	presupuesto=float(eth_balance["free"])
except:	
	print("Error de conexion")

moneda="BNBEUR"
info=cliente.get_symbol_ticker(symbol=moneda)
print(info)

precio_compra=float(info["price"])



def orden_de_comprar(presupuesto,precio_compra):
	precio_compra=float(precio_compra)
	print(precio_compra)
	print(cliente.get_symbol_info(moneda))
	cantidad_quantily=0	
	if presupuesto>11 and presupuesto*0.1>11:
		cantidad_gasto=0.1*presupuesto
		
	else:
		cantidad_gasto=12
	precio_alto=round(precio_compra*1.001,2)
	precio_bajo=round(precio_compra*0.999,2)	

	cantidad_quantily=(cantidad_gasto/precio_bajo)
	cantidad_quantily=round(cantidad_quantily,2)
	
	cantidad_gasto=cantidad_quantily*precio_bajo
			
	decimales=2
	orden_compra=cliente.order_oco_buy(
					symbol=moneda,
					quantity= cantidad_quantily,                                            
				    price=str(round(precio_bajo,2)),                                            
				    stopPrice= str(round(precio_alto,2)),                                            
				    stopLimitPrice=str(round(precio_alto*0.99,2)),                                            
				    stopLimitTimeInForce='GTC'
                	)

	print(orden_compra)
	return()










orden_de_comprar(presupuesto,precio_compra)

