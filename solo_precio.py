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

cliente=Client(usuario1.api_key,usuario1.secret_key, tld='com')

def cerrar_market(tipo_compra):
	a=True
	cliente.futures_cancel_all_open_orders(symbol=moneda)	
	
	if tipo_compra=='SELL':
		side_cancelacion='BUY'

	elif tipo_compra=='BUY':
		side_cancelacion='SELL'	
	else:
		print("No se puede cancelar la operacion")
			
	print("Se incia la cancelacion")	
	while a==True:
		try:
			
			result_1 = cliente.futures_symbol_ticker(symbol=moneda)
			precio_3=float(result_1['price'])
			quan=11/precio_3
			precio_3=round(precio_3,4)
			quan=round(quan,0)	
			
			#---------------------------------------------------------------------
			cancelacion=cliente.futures_create_order(
				symbol=moneda,
				side=side_cancelacion,
				type='TAKE_PROFIT_MARKET',
				timeInForce='GTC',
				stopPrice=precio_3,
				closePosition=True,
				 )
		 
			print(cancelacion)
			time.sleep(5)
			
			inversion=comprobar_balance()			
			if inversion==0:
				a=False
			else:
				a=True
				time.sleep(5)

		except Exception as e:
			print("Va ser que no  va: ",e)
			inversion=comprobar_balance()			
			if inversion==0:
				a=False
			else:
				a=True
	cliente.futures_cancel_all_open_orders(symbol=moneda)	

def comprobar_balance():
	a=0
	magin1=cliente.futures_account_balance(symbol=moneda)			
	balance=magin1[1]
	presupuesto=float(balance['balance'])
	inversion=float(balance['withdrawAvailable'])
	a= presupuesto-inversion
	return (a)



estado=''
precio_compra=0
it=0
precio_1=0
precio_2=0
tipo_compra='nada'
tipo=''


while 1:
	try:
		print(precio_compra)
			
		if it==0:
			balance_total=cliente.futures_account_balance()
			balance_usdt=balance_total[1]
			balance_price=float(balance_usdt['balance'])
			print("El presupuesto inicial es de :",balance_price)
			result_1 = cliente.futures_symbol_ticker(symbol='DOGEUSDT')
			precio_2=float(result_1['price'])
			print("Nº1: ",precio_2)
			precio_1=0
			moneda='DOGEUSDT'
			it+=1


		if precio_compra>0:
			moneda='DOGEUSDT'
			if precio_1==0:
				balance_total=cliente.futures_account_balance()
				balance_usdt=balance_total[1]
				balance_despues_compra=float(balance_usdt['balance'])
				print("Mi presupuesto es de: ",balance_despues_compra)
				time.sleep(2)
			if it/10==int(it/10):
				inversion=comprobar_balance()
				if inversion<0:
					break
				elif inversion==0:
					it=0
					precio_compra=0
					tipo_compra='nada'
					

			time.sleep(2)
			precio_1=0
				
		it+=1
		medir=0		
		while precio_1==0 or precio_1==precio_2:
			medir+=1
			time.sleep(0.4*medir)
			result_1 = cliente.futures_symbol_ticker(symbol=moneda)
			precio_1=float(result_1['price'])
			time.sleep(0.1*medir)
		cliente.futures_cancel_all_open_orders(symbol=moneda)	
		print("Nº1: ",precio_1)
		print("--------------------------------------")
		time.sleep(0.3)

		if precio_compra==0 :			
			direrencia=precio_1-precio_2
			print("-----------",direrencia,"----------")
			incremento=(direrencia/precio_1)*100
			
			print("------------",incremento,"---------")
			if incremento>0.05:
				print("!!!!orden de venta o short")
				tipo='BUY'
			elif incremento<=-0.05:
				print("!!!!orden de compra o long")
				tipo='SELL'
			else:
				tipo=''	
				

		precio_2=precio_1

		if tipo!='' and it>2 :
			inversion=comprobar_balance()
			if inversion!=0 and tipo_compra=='nada':
				print(inversion)
				print(tipo_compra)
				print("opcion 1")
				tipo_compra='nada'
				precio_compra=0
				it=0 
				it=0
				
			elif inversion!=0 and tipo_compra!='nada':	
				print("opcion 2")
				stop_market(precio_compra)
			
			elif inversion==0 and tipo_compra=='nada' :
				print("Se da orden: ",tipo)
				moneda='DOGEUSDT'
								
				result_1 = cliente.futures_symbol_ticker(symbol=moneda)
				precio_3=float(result_1['price'])
				quan=7/precio_3
				quan=round(quan,0)
				
#ORDEN DE COMPRA------------------------------------------------------------	
				cliente.futures_cancel_all_open_orders(symbol=moneda)
				
				nueva_orden=cliente.futures_create_order(
					symbol=moneda,
					side=tipo,
					quantity=quan ,
					type='MARKET',
					)
#----------------------------------------------------------------------------------------
				time.sleep(7)
				print(nueva_orden)
				identificacion=nueva_orden['orderId']
				orden_precio=cliente.futures_get_order(symbol=moneda, orderId=int(identificacion))
				print(orden_precio)
				precio_compra=float(orden_precio['avgPrice'])
				print(precio_compra)
				inversion=comprobar_balance()			
				if inversion>0:
					print("----------Se hizo la inversion {}---------".format(tipo))
				elif inversion<0:
					print("----------No se hizo la inversion-------")
					precio_compra=0
					it=0
					break
				time.sleep(5)
				tipo_compra=tipo
				tipo=''
				precio_1=0
			
			else:
				tipo_compra='nada'	
		
##CIERRE DE OPERACION------------------------------------------------------------------------------------------------------
		if precio_1!=0:

			if tipo_compra!='':
				print("El precio de compra = {} \n el de mercado = {} \n tipo= {}".format(precio_compra,precio_1,tipo_compra) )		
				time.sleep(2)

			if tipo_compra=='SELL':
				if precio_compra<precio_1:
					if precio_compra*1.001<(precio_1):
						cerrar_market(tipo_compra)
						tipo_compra='nada'
						precio_compra=0
						it=0
				elif it>10 and precio_compra<1.005*precio_1:
					if precio_compra<1.001*precio_1 and precio_compra>1.0001*precio_1:
						cerrar_market(tipo_compra)
						tipo_compra='nada'
						precio_compra=0
						it=0

				elif precio_compra>1.005*precio_1:
					precio_compra=1.004*precio_1
					magin1=cliente.futures_account_balance(symbol=moneda)			
					balance=magin1[1]
					inversion=round(float(balance['withdrawAvailable']),2)
					try:

						if inversion>0:
							result=cliente.futures_change_position_margin(symbol=moneda,amount=str(inversion),type=1)
						print(result)
					except:
						print("no se pudo")	

					print("Se cambiaron los valores------------")
					time.sleep(1)				

			if tipo_compra=='BUY':
				if precio_compra>precio_1:
					if precio_compra>(precio_1*1.001):
						cerrar_market(tipo_compra)
						tipo_compra='nada'
						precio_compra=0
						it=0
				elif it>10 and precio_compra*1.005>(precio_1):
					if precio_compra*1.001>precio_1 and precio_compra*1.0001<precio_1:
						cerrar_market(tipo_compra)
						tipo_compra='nada'
						precio_compra=0
						it=0 
				elif precio_compra<0.995*precio_1:
					precio_compra=0.996*precio_1
					magin1=cliente.futures_account_balance(symbol=moneda)			
					balance=magin1[1]
					inversion=round(float(balance['withdrawAvailable']),2)
					try:

						if inversion>0:
							result=cliente.futures_change_position_margin(symbol=moneda,amount=str(inversion),type=1)
						print(result)
					except:
						print("no se pudo ")	

					print("Se cambiaron los valores------------")
					time.sleep(1)				
			time.sleep(0.3)


	except Exception as e:
		time.sleep(10)
		print('ERROR',e)
		time.sleep(10)	
		it=0
		if e=='APIError(code=-2019): Margin is insufficient.':
			cerrar_market(tipo_compra)







