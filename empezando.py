from binance.client import Client
import usuario1 
from binance import ThreadedDepthCacheManager
from binance import BinanceSocketManager
from binance import DepthCacheManager
from binance import *
import time
import numpy as np

cliente=Client(usuario1.api_key,usuario1.secret_key)
moneda="BNBEUR"

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




def compra(precio_compra,presupuesto):
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


def cancelar_venta(numero_orden):
	result = cliente.cancel_order(symbol=moneda, orderId='orderId')
	print(result)
	return result


def inicio():
	cliente=Client(usuario1.api_key,usuario1.secret_key)
	presupuesto_balance = cliente.get_asset_balance(asset='EUR')
	print(presupuesto_balance)
	print("Mi presupuesto de ETH: ",presupuesto_balance["free"])
	moneda="BNBEUR"

def libro_ordenes():
	info=cliente.get_symbol_ticker(symbol=moneda)
	profundidad=cliente.get_order_book(symbol=moneda)
	precio=float(info["price"])
	it=0
	valor_libro=0
	total_libro_compras=0
	total_libro_ventas=0
	while it<2:
		precio_debajo_5=(float(precio))*0.995
		precio_arriva_5=(float(precio))*1.005
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
		time.sleep(2)		

	total_libro=100*(total_libro_compras/(total_libro_compras+total_libro_ventas))-50
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
	historico=cliente.get_historical_klines(moneda, Client.KLINE_INTERVAL_1MINUTE,"1 hour ago UTC")
	historico=np.array(historico)
	#print(historico[0,:])
	for i in range(0,len(historico)):
		a=float(historico[i][2])
		x.append(i)
		y.append(a)
		
	curva1=np.polyfit(x,y,2)
	actual_real=float(historico[0,1])
	anterior_real=float(historico[1,1])
	suma_real=actual_real-anterior_real
	siguiente=curva1[0]*((len(x)+1)**2)+curva1[1]*(len(x)+1)+curva1[2]
	actual_curva=curva1[0]*(len(x)**2)+curva1[1]*(len(x))+curva1[2]
	error=actual_real-actual_curva
	#print(suma_real,curva1[0])
	if suma_real<0:
		print("Estaba decreciendo")
	else:
		print("Estaba creciendo")	
	time.sleep(2)

	if curva1[0]>0 and  suma_real>0:
		print("Esta creciendo el valor es {} y sera {} se esta comprando ".format(actual_real,(siguiente+error)))
		return "creciendo"
	elif curva1[0]<0 and suma_real<0:
		print("Esta decreciendo el valor es {} y sera {} se esta vendiendo ".format(actual_real,(siguiente+error)))
		return "decreciendo"
	else:
	 time.sleep(2)
	 print("zs")		
	#print(curva(0))	

def media_dos_horas():
	historico=cliente.get_historical_klines(moneda, Client.KLINE_INTERVAL_1MINUTE,"2 hour ago UTC")
	historico=np.array(historico)
	#print(historico[0,:])
	suma=0
	media_2h=0
	for i in range(0,len(historico)):
		a=float(historico[i][2])
		suma=suma+a
	media_2h=suma/len(historico)
	print("La media de las ultimas 2h es:",media_2h)
	return media_2h


def conexion_ping(cliente):
	operacion_online=False
	conexion=False
	cliente_online=False
	pagina=0
	pagina=cliente.ping()
	#print("La resouesta es: ",pagina)
	status = cliente.get_system_status()
	estado=status['msg']
	if pagina!=0:
		tiempo1=cliente.get_server_time()
		tiempo2=cliente.get_server_time()
		tiempo_respuesta=tiempo2["serverTime"]-tiempo1["serverTime"]
		#print(tiempo_respuesta)
		if tiempo_respuesta<1000:
			conexion=True
		else: conexion=False
	else: 
		conexion=False
		print("Error de conexion")
	if conexion==True and estado=="normal":
		operacion_online=True	
	return operacion_online	

conexion=(conexion_ping(cliente))
print(conexion)
#conexion True, es que esta bien

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
	try:

		try:
			if conexion_binance==False:
				time.sleep(30)
				inicio()
			conexion=(conexion_ping(cliente))
			if conexion==False:
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

			compra_balance = cliente.get_asset_balance(asset="EUR")
			print(compra_balance)
			venta_balance=cliente.get_asset_balance(asset="BNB")
			print(venta_balance)
					
			presupuesto=float(compra_balance["free"])
			ordernes_abiertas = cliente.get_open_orders(symbol=moneda)
			if len(ordernes_abiertas)!=0:
				ordenes=1
			else:
				ordenes=0	

			order = cliente.create_test_order(
			    symbol=moneda,
			    side="BUY",
			    type="LIMIT",
			    timeInForce="GTC",
			    quantity=100,
			    price='100')
			print("El test la orden sale: ",order)


		if ordenes==1 or ordenes==-1:
			ordenes_abiertas=cliente.get_open_orders(symbol=moneda)
			if ordernes_abiertas!=[]:
				print(len(ordernes_abiertas))
				for i in ordenes_abiertas:
					for j in i:
						if j=="orderId":
							numero_orden=i[j]
						elif j=="price":
							precio_precompra=float(i[j])
						elif j=="side":
							tipo=i[j]		
				precio_compra=precio_precompra			
				print("La orden esta abierta es de tipo {}, tiene el numero {}, al precio de {}".format(tipo,numero_orden,precio_precompra))
			else:
				precio_precompra=0	
			
		time.sleep(1)
		info=cliente.get_symbol_ticker(symbol=moneda)
		print(info["price"])
		precio_1=float(info["price"])
		time.sleep(2)
		condicion_1=tendencia()
		condicion_2=libro_ordenes()
		condicion_3=0.998*(media_dos_horas())	
		time.sleep(2)

		compra_balance = cliente.get_asset_balance(asset="EUR")
		presupuesto_compra=float(compra_balance["free"])
		presupuesto_comprando=float(compra_balance["locked"])
		print("El dinero para poder comprar es de {} y se estan invirtiendo {}".format(presupuesto_compra,presupuesto_comprando))

		venta_balance=cliente.get_asset_balance(asset="BNB")
		presupuesto_venta=float(venta_balance["free"])
		presupuesto_vendiendo=float(venta_balance["locked"])
		print("El dinero para poder vender es de {} y se estan invirtiendo {}".format(presupuesto_venta,presupuesto_vendiendo))

		info=cliente.get_symbol_ticker(symbol=moneda)
		print(info["price"])
		precio_2=float(info["price"])
		suma_precio=(precio_1)-(precio_2)
		media_precio=(precio_1+precio_2)/2
		
		
		if presupuesto_venta>(10/precio_2):
			ordenes=-1
			
		else:
			if presupuesto_vendiendo>(10/precio_2) or presupuesto_comprando>10:
				ordenes=1
			else:
				ordenes=0	
		print("la media es de {} y la media de las ultimas 2h es: {}".format(media_precio,condicion_3))		
		if ordenes==0 and media_precio>condicion_3:
			suma_precio=-1	
			
		print("El precio teorico de operacion es de:", precio_compra)
		time.sleep(1)
		print("Las ordenes son: ",ordenes)
		print("La suma sale: ",suma_precio)
		
		if suma_precio>0 and ordenes==0:
			if (condicion_1=="decreciendo" or condicion_2=="libro_ordenes_compra"):
				print("----Se da la instrucion de compra--------{},{}".format(precio_1,precio_2))
				info_precio_compra=cliente.get_symbol_ticker(symbol=moneda)
				precio_compra=float(info_precio_compra["price"])
				(orden_compra)= compra(precio_compra,presupuesto)
				print(precio_compra)
				ordenes=1
				it=0
				tiempo_compra=time.time()
				continue
					
		elif (precio_compra)*1.005<=precio_2 and ordenes==-1:
			if condicion_1=="creciendo" or condicion_2=="libro_ordenes_venta":
					print("----Se da la instrucion de venta--------",precio_compra)
					info_precio_venta=cliente.get_symbol_ticker(symbol=moneda)
					precio_venta=precio_compra*1.005
					orden_venta=venta(precio_venta)
					print("Se compro a {} y se vendio a {}".format(precio_compra,precio_venta))
					tiempo_compra=0

					ordenes=1
						
		else:
			time.sleep(3)	
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
		inicio()
		continue	
