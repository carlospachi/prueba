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
moneda="BTCEUR"

try:
	presupuesto_balance = cliente.get_asset_balance(asset='EUR')
	print(presupuesto_balance)
	print("Mi presupuesto de BTC: ",presupuesto_balance["free"])
	presupuesto=float(presupuesto_balance["free"])
except:	
	print("Error de conexion")

info = cliente.get_open_orders(symbol=moneda )
print(info)
info=cliente.get_symbol_ticker(symbol=moneda)
precio=float(info["price"])
print(precio)


def compra(precio_compra,presupuesto):
	precio_compra=float(precio_compra)
	print(precio_compra)
	print(cliente.get_symbol_info(moneda))
	cantidad_quantily=0	
	if presupuesto>11 and presupuesto*0.1>11:
		cantidad_gasto=0.1*presupuesto
	else:
		cantidad_gasto=12
	precio_bajo=round(precio_compra*0.999,0)
	precio_alto=round(precio_compra*1.001,0)
	cantidad_quantily=round(float(cantidad_gasto/precio_bajo),6)
	cantidad_quantily=str(cantidad_quantily)
	print(cantidad_quantily)
	print(precio_bajo)
	print(precio_alto)
	precio_price=str(precio_alto)

	orden_compra=cliente.order_limit_buy(symbol=moneda, quantity=cantidad_quantily, price=precio_price)
	time.sleep(15)
	print(orden_compra)
	return(orden_compra,precio_price)




a,b=compra(precio,presupuesto)
