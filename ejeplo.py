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
print(precio_compra)
decimales=11
redondeo="{:.8f}"
info = cliente.get_symbol_info(moneda)
print(info)
#cantidad=redondeo.format(round(0.01*presupuesto,decimales))
cantidad=0.1*presupuesto
print(cantidad)
precio=redondeo.format(round(precio_compra*1.02,decimales))
print(precio)
precio_perdidas=redondeo.format(round(precio_compra*0.95,decimales))
print(precio_perdidas)

def orden_de_comprar():
	orden = cliente.create_test_order(
		    symbol=moneda,
		    side="BUY",
		    type="LIMIT",
		    timeInForce="GTC",
		    quantity=100,
		    price='100')
	print("El test la orden sale: ",orden)	




	orden_compra=cliente.order_limit_buy(
				symbol=moneda,
				quantity=0.36,
				price='100')

	print(orden_compra)
	return()



orden_de_comprar()
"""
time.sleep(10)
print(orden_compra)
info=cliente.get_symbol_ticker(symbol=moneda)
print(info["price"])
precio_compra_nueva=float(info["price"])

while precio_compra>precio_compra_nueva:
	precio_compra=precio_compra_nueva
	orden_de_comprar()

	time.sleep(10)
	info=cliente.get_symbol_ticker(symbol=moneda)
	print(info["price"])
	precio_compra_nueva=float(info["price"])
	print(orden_compra)	

cancel_order=cliente.cancel_order(
	symbol=moneda,
	order_id=order[0].get("orden_compra"))
print(cancel_order)


"""



