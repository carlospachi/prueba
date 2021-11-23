from binance.client import Client
import usuario1 
from binance import ThreadedDepthCacheManager
from binance import BinanceSocketManager
from binance import DepthCacheManager
from binance import *
import time
import numpy as np



cliente=Client(usuario1.api_key, usuario1.secret_key, tld="com")
moneda="DOGEUSDT"

"""
def venta(precio_venta):
	try:
		venta_balance = cliente.get_asset_balance(asset='BNB')
		print(venta_balance)
		print("Mi presupuesto es: ",venta_balance["free"])
		presupuesto=float(venta_balance["free"])
	except:	
		print("Error de conexion")
	info=cliente.get_symbol_ticker(symbol=moneda)
	precio_mercado=float(info["price"])
	if precio_venta<precio_mercado:
		precio_venta=precio_mercado	
	
	presupuesto=round(float(venta_balance["free"]),4)
	precio_venta=round(precio_venta*1.001,2)
	precio_price=str(precio_venta)
	orden_venta=cliente.order_limit_sell(symbol=moneda, quantity=str(presupuesto), price=precio_price)
	time.sleep(15)
	print(orden_venta)
	return(orden_venta)
"""


"""
def compra(precio_compra):
	presupuesto_balance = cliente.get_asset_balance(asset='EUR')
	presupuesto_balance=presupuesto
	precio_compra=float(precio_compra)
	print(precio_compra)
	print(cliente.get_symbol_info(moneda))
	info=cliente.get_symbol_ticker(symbol=moneda)
	precio_mercado=float(info["price"])
	if precio_compra>precio_mercado:
		precio_compra=precio_mercado
	cantidad_quantily=0	
	if presupuesto>11 and presupuesto*0.1>11:
		cantidad_gasto=0.1*presupuesto
	else:
		cantidad_gasto=12
	precio_bajo=round(precio_compra*0.999,2)
	precio_alto=round(precio_compra*1.001,2)
	cantidad_quantily=round(float(cantidad_gasto/precio_bajo),3)
	cantidad_quantily=str(cantidad_quantily)
	precio_price=str(precio_bajo)

	orden_compra=cliente.order_limit_buy(symbol=moneda, quantity=cantidad_quantily, price=precio_price)
	time.sleep(15)
	print(orden_compra)
	return(orden_compra)
"""

"""
def cancelar_venta(numero_orden):
	result = cliente.cancel_order(symbol=moneda, orderId='orderId')
	print(result)
	return result
"""

def inicio():
	cliente=Client(usuario1.api_key,usuario1.secret_key, tld="com")
	moneda="DOGEUSDT"
	print(cliente.get_account_status())
	print("sale el ping: ",(cliente.futures_ping()))
	print(cliente.futures_symbol_ticker(symbol=moneda))

	print(cliente.futures_mark_price(symbol=moneda))
	
	return 


def libro_ordenes(x):
	result = cliente.futures_symbol_ticker(symbol=moneda)
	precio=float(result['price'])

	profundidad=cliente.futures_order_book(symbol=moneda)
	x_arriva=(100+(x/10))/100
	x_abajo=(100-(x/10))/100
	it=0
	valor_libro=0
	total_libro_compras=0
	total_libro_ventas=0
	while it<2:
		precio_debajo_5=(float(precio))*x_abajo
		precio_arriva_5=(float(precio))*x_arriva
		compras=(profundidad["bids"])
		
		for i in range(0,len(compras)):
			valores=compras[i]
			valor_precio=float(valores[0])
			valor_libro=float(valores[1])
			if valor_precio>precio_debajo_5:
				total_libro_compras+=valor_libro


		compras=(profundidad["asks"])
		
		for i in range(0,len(compras)):
			valores=compras[i]
			valor_precio=float(valores[0])
			valor_libro=float(valores[1])
			if valor_precio<precio_arriva_5:
				total_libro_ventas+=valor_libro
		it+=1
				

	total_libro=100*(total_libro_compras/(total_libro_compras+total_libro_ventas))-50
	total_libro=round(total_libro,4)
	total_libro_compras=round(total_libro_compras,4)
	total_libro_ventas=round(total_libro_ventas,4)
	print("Las compras respecto a las ventas es de: {} las compras son: {}, y las ventas son: {} ".format(total_libro,total_libro_compras,total_libro_ventas))
	if total_libro<(-5):
		return "libro_ordenes_compra"
	elif total_libro>5:
		return "libro_ordenes_venta"	

	else:
		time.sleep(2)
		print("z")	


def tendencia():
	time.sleep(1)
	x=[]
	y=[]
	historico=cliente.futures_historical_klines(moneda, Client.KLINE_INTERVAL_1MINUTE,"1 hour ago UTC")
	historico=np.array(historico)
	#print(historico[0,:])
	for i in range(0,len(historico)):
		a=float(historico[i][2])
		x.append(i)
		y.append(a)
		
	curva1=np.polyfit(x,y,2)
	actual_real=round(float(historico[0,1]),4)
	anterior_real=float(historico[1,1])
	suma_real=actual_real-anterior_real
	siguiente=round(curva1[0]*((len(x)+1)**2)+curva1[1]*(len(x)+1)+curva1[0],4)
	actual_curva=curva1[0]*(len(x))+curva1[1]*(len(x))+curva1[0]
	error=round(actual_real-actual_curva,4)
	#print(suma_real,curva1[0])
	tiempo_conclusion_tendencia=time.time()
	if suma_real<0:
		print("Estaba decreciendo donde es: -{}x+{}=y".format(round(curva1[0],4),round(curva1[1],4)))
		
	else:
		print("Estaba creciendo donde es: +{}x+{}=y".format(round(curva1[0],4),round(curva1[1],4)))

	time.sleep(2)

	if curva1[0]>0 and  suma_real>0:
		print("Esta creciendo el valor es {} y sera {} se esta comprando ".format(actual_real,(siguiente+error)))
		return ("creciendo",tiempo_conclusion_tendencia)
	elif curva1[0]<0 and suma_real<0:
		print("Esta decreciendo el valor es {} y sera {} se esta vendiendo ".format(actual_real,(siguiente+error)))
		return ("decreciendo",tiempo_conclusion_tendencia)
	else:		
		 time.sleep(2)
		 print("zs")
		 return ("Estaba sube y baja",tiempo_conclusion_tendencia)
		
		


def media_x_horas():
	
	historico=cliente.futures_historical_klines(moneda, Client.KLINE_INTERVAL_1MINUTE,"1 hour ago UTC")
	historico=np.array(historico)
	#print(historico[0,:])
	suma=0
	media_xh=0
	for i in range(0,len(historico)):
		a=float(historico[i][2])
		suma=suma+a
	media_xh=suma/len(historico)
	media_xh=round(media_xh,4)
	print("La media de las ultimas 2h es:",media_xh)
	tiempo_conclusion_x_horas=time.time()
	return (media_xh,tiempo_conclusion_x_horas)


conexion=cliente.futures_ping()
print(conexion)
conexion=True
status = cliente.get_system_status()
print(status)

it=0
conexion_binance=True
precio_compra=10000
precio_precompra=0
ordenes=0
tiempo_compra=0
tiempo_inicio_compra=0
media_precio=0


while conexion==True:
	print(it)
	try:

		try:
			if conexion_binance==False:
				time.sleep(30)
				inicio()
				pings=cliente.futures_ping()
				if pings=={}:
					conexion=True
				else:
					conexion=False	
						
			elif conexion==False:
				print("ERROR DE CONEXION")
				time.sleep(30)
				conexion=True 
				continue

		except:
			time.sleep(30)
			print("Error")
			conexion_binance=False
			continue

		if it==0:
			print("Por ahora no se hace balance de cuantas")
			presupuesto=cliente.futures_account_balance(asset='USDT')
			presupuesto_usd=presupuesto[1]
			presupuesto_usd_total=presupuesto_usd['balance']
			presupuesto_usd_sininvertir=presupuesto_usd['withdrawAvailable']
				
			
			ordernes_abiertas = cliente.futures_get_open_orders()
			if len(ordernes_abiertas)!=0:
				ordenes=1
			else:
				ordenes=0
			tiempo_conclusion_tendencia=0
			tiempo_conclusion_x_horas=0		

			
		if ordenes==1 or ordenes==-1:
			ordenes_abiertas=cliente.futures_get_open_orders()
			if ordernes_abiertas!=[]:
				print((ordernes_abiertas))
				
				precio_precompra=0	
		

#CONDICIONES------------------------------------------------------------------------------

		time.sleep(1)
		result = cliente.futures_symbol_ticker(symbol=moneda)
		precio_1=float(result['price'])
		print(precio_1)

		tiempo_actual=time.time()
		time.sleep(2)
		if (tiempo_actual- tiempo_conclusion_tendencia)>60:
			(condicion_1,tiempo_conclusion_tendencia)=tendencia()
		else:
			time.sleep(2)	
			
		condicion_2=libro_ordenes(5)

		tiempo_actual=time.time()
		if (tiempo_actual- tiempo_conclusion_x_horas)>60:
			condicion_3,tiempo_conclusion_x_horas=(media_x_horas())
		else:
			time.sleep(2)		
		time.sleep(2)

		if condicion_1=='creciendo':
			print("Tocaria condicon LONG")
		elif condicion_1=='decreciendo':
			print("Tocaria condicion SHORT")	


		presupuesto=(cliente.futures_account_balance(asset='USDT'))
		presupuesto_usd=presupuesto[1]
		presupuesto_usd_total=float(presupuesto_usd['balance'])
		presupuesto_usd_sininvertir=float(presupuesto_usd['withdrawAvailable'])
		presupuesto_usd_invertido=presupuesto_usd_total-presupuesto_usd_sininvertir
		
		print("El dinero para poder comprar es de {} y se estan invirtiendo {}".format(presupuesto_usd_total,presupuesto_usd_invertido))

		result = cliente.futures_symbol_ticker(symbol=moneda)
		precio_2=float(result['price'])
		print(precio_2)
		suma_precio=(precio_1)-(precio_2)
		media_precio=(precio_1+precio_2)/2
		
		
		if presupuesto_usd_invertido>(10):
			ordenes=-1
			
		else:
			if presupuesto_usd_invertido>(10) :
				ordenes=1
			else:
				ordenes=0

		print("la media es de {} y la media de las ultimas 2h es: {} ".format(media_precio, condicion_3))		
		if ordenes==0 and media_precio>condicion_3:
			suma_precio=-1	
			
		print("El precio teorico de operacion es de:", precio_2)
		time.sleep(1)
		print("Las ordenes son: ",ordenes)
		print("La suma sale: ",suma_precio)
		
#SE COMPRA REALIZA LA ACCION----------------------------------------------------------------------------------------

		if suma_precio>0 and ordenes==0:
			if (condicion_1=="decreciendo" or condicion_2=="libro_ordenes_compra"):
				print("----Se da la instrucion de compra--------{},{}".format(precio_1,precio_2))
				result = cliente.futures_symbol_ticker(symbol=moneda)
				precio_compra=float(result['price'])
				#(orden_compra)= compra(precio_compra)
				#print(orden_compra)
				ordenes=1
				it=0
				tiempo_compra=time.time()
				continue

					
		elif (precio_compra)*1.005<=precio_2 and ordenes==-1:
			if condicion_1=="creciendo" or condicion_2=="libro_ordenes_venta":
					print("----Se da la instrucion de venta--------",precio_compra)
					result = cliente.futures_symbol_ticker(symbol=moneda)
					precio_compra=float(result['price'])
					precio_venta=precio_compra*1.005
					#orden_venta=venta(precio_venta)
					print("Se compro a {} y se vendio a {}".format(precio_compra,precio_venta))
					tiempo_compra=0

					ordenes=1
						
		
		

		else:
			time.sleep(3)	
			if tiempo_compra>0:
				tiempo_actual=time.time()
				tiempo_operacion=tiempo_actual-tiempo_compra
				print(tiempo_operacion)	
				if tiempo_operacion>7200 and media_precio<(precio_compra)*0.95:
					print("------------Se canceló la orden de compra:---------------")	
					ordenes=0
					tiempo_compra=0
					precio_compra=0

		precio_compra=precio_precompra
		print("----------------------------------------------------")		
		it+=1
		time.sleep(1)

	except Exception as e:
		print(e)
		time.sleep(30)
		it=0
		inicio()
		continue	







