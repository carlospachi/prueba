from binance.client import Client
import usuario1 
from binance import ThreadedDepthCacheManager
from binance import BinanceSocketManager
from binance import DepthCacheManager
from binance import *
import time
import numpy as np



#def lista_mercados_operativos(lista_de_mercados)
#MONEDA =['MERCADO','MONEDA_COMPRA','MONEDA_VENDE',DECI_QUA_COMPRA,DECI_PRICE,COMPRA,DECI_QUA_VENTA,DECI_PRICE_VENTA]

#lista_mercados=[BNBEUR,CHZUSDT]

#BNBEUR=OPERCION('BNBEUR','EUR','BNB',3,2,4,2,)
#CHZUSDT=OPERCION("CHZUSDT", "USDT","CHZ",1,4,1,4)





cliente=Client(usuario1.api_key,usuario1.secret_key)

def conexion():
	conexion_binance="OFF"
	cliente=Client(usuario1.api_key ,usuario1.secret_key)
	dato=cliente.ping()
	status = cliente.get_system_status()
	if status["status"]==0 and status["msg"]=="normal":
		conexion_binance="ON"
	else:
		conexion_binance="OFF"	
	
	return conexion_binance	

def consulta_binance():
	if conexion()=="ON":
		print("ok")
		

class MERCADO():
			
	def __init__(self,moneda,moneda_compra,moneda_venta):
		cliente=Client(usuario1.api_key ,usuario1.secret_key)
		self.moneda=moneda
		self.moneda_compra=moneda_compra
		self.moneda_venta=moneda_venta
		self.precio_actual=cliente.get_symbol_ticker(symbol=moneda)['price']
		self.presupuesto_compra= cliente.get_asset_balance(asset=moneda_compra)['free']
		self.presupuesto_venta=  cliente.get_asset_balance(asset=moneda_venta)['free']
		self.inversion_compra=  cliente.get_asset_balance(asset=moneda_compra)['locked']
		self.inversion_venta= cliente.get_asset_balance(asset=moneda_venta)['locked']

	
	def __str__(self):
		return (str(self.moneda)+" "+str(self.precio_actual))
		
	def libro_ordenes(self,tolerancia_por100):
		total_libro_compras=0
		total_libro_ventas=0
		
		profundidad=cliente.get_order_book(symbol=self.moneda)
		precio_pordebajo=float(self.precio_actual)*(100-tolerancia_por100)/100
		precio_porencima=float(self.precio_actual)*(100+tolerancia_por100)/100
		compras=profundidad['bids']
		ventas=profundidad['asks']
		it=0
		while it<=3:
			for i in range(0,len(compras)):
				valores_compras=compras[i]
				valor_precio_compras=float(valores_compras[0])
				valor_libro_compras=float(valores_compras[1])
				if valor_precio_compras>precio_pordebajo:
					total_libro_compras+=valor_libro_compras
			for i in range(0,len(ventas)):
				valores_ventas=ventas[i]
				valor_precio_ventas=float(valores_ventas[0])
				valor_libro_ventas=float(valores_ventas[1])
				if valor_precio_ventas<precio_porencima:
					total_libro_ventas+=valor_libro_ventas		

			time.sleep(2)		
			it+=1		

		relacion=100*total_libro_ventas/(total_libro_compras+total_libro_ventas)-50
		self.relacion
		
		return relacion

	def media_ponderada(self,tiempo_porhoras):	
		tiempo_porhoras=str(tiempo_porhoras)
		self.maximo=0
		self.minimo=0
		self.media=0

		historico=cliente.get_historical_klines(self.moneda, Client.KLINE_INTERVAL_1MINUTE,tiempo_porhoras+" hour ago UTC")
		historico=np.array(historico)
		#print(historico[0,:])
		suma=0
		
		it=0
		for i in range(0,len(historico)):

			a=float(historico[i][2])
			if a>=self.maximo:
				self.maximo=a
			if it<1:
				self.minimo=a
			elif a<self.minimo:
				self.minimo=a	 	
			
			suma=suma+a
			it+=1
		self.media=suma/len(historico)

		self.maximo
		self.minimo
		self.media
		return (self.maximo,self.media,self.minimo)

		
	def tendencia(self,tiempo_horas):
		tiempo_horas=str(tiempo_horas)
		x=[]
		y=[]
		historico=cliente.get_historical_klines(self.moneda, Client.KLINE_INTERVAL_1MINUTE,tiempo_horas+" hour ago UTC")
		historico=np.array(historico)
		for i in range(0,len(historico)):
			a=float(historico[i][2])
			x.append(i)
			y.append(a)
			
		curva1=np.polyfit(x,y,2)
		actual_real=float(historico[0,1])
		anterior_real=float(historico[1,1])
		suma_real=actual_real-anterior_real
		if suma_real<0.0001*actual_real:
			suma=0
		siguiente=curva1[0]*((len(x)+1)**2)+curva1[1]*(len(x)+1)+curva1[2]
		actual_curva=curva1[0]*(len(x)**2)+curva1[1]*(len(x))+curva1[2]
		
		if suma_real<0:
			if curva1[0]<0 and curva1[1]<0:
				return "decreciendo mucho"
			elif curva1[0]>0 and curva1[1]>0:
				return "decreciendo mucho"	
			else:
				return "decreciendo"
		elif suma_real>0:
			if curva1[0]>0 and curva1[1]<0:
				return "creciendo mucho"
			elif curva1[0]<0 and curva1[1]>0:
				return "creciendo mucho"
			else:
				return "creciendo"
		else:
			return "Z"
		


class OPERCION(MERCADO):
	

	def __init__(self,moneda,moneda_compra,moneda_venta,dec_qua_compra,dec_price_compra,dec_qua_venta,dec_price_venta):
		super().__init__(moneda,moneda_compra,moneda_venta)
		self.dec_qua_compra=dec_qua_compra
		self.dec_price_compra=dec_price_compra
		self.dec_qua_venta=dec_qua_venta
		self.dec_price_venta=dec_price_venta
		self.orden_abierta=False

	def ordenes_abiertas(self):
		lista_ordenes_hechas=cliente.get_open_orders(symbol=self.moneda)
		if len(lista_ordenes_hechas)>0:
			self.orden_abierta=True
		return lista_ordenes_hechas	
			

	def compra_limite(self,precio,limite):
		limite=float(limite)
		if limite>float(self.presupuesto_compra):
			return "Error, no hay presupuesto"
		else:
			if  self.moneda_compra=="EUR" or self.moneda_compra=='USDT':
				if limite<11 and limite!=0:
					return "Error, cantidad insuficiente"
				elif limite==0:
					limite=12
						
		if float(self.precio_actual)<float(precio):
			precio=precio_actual

		cantidad_quantily=0	
		precio_bajo=round(float(precio)*0.999,self.dec_price_compra)
		cantidad_quantily=round(float(limite/precio_bajo),self.dec_qua_compra)
		cantidad_quantily=str(cantidad_quantily)
		precio_price=str(precio_bajo)

		orden_compra=cliente.order_limit_buy(symbol=self.moneda, quantity=cantidad_quantily, price=precio_price)
		time.sleep(15)
		self.orden_compra
		
		return(orden_compra)	
		

	def venta_limite(self,precio,limite):
		limite=round(float(limite),self.dec_qua_venta )
		if limite>float(self.presupuesto_venta) and limite!=0:
			return "Error, no tienes esa cantidad"
		elif limite==0:
			limite=round(float(self.presupuesto_venta),self.dec_qua_venta)


		if float(self.precio_actual)>float(precio):
			precio=round(float(precio_actual),self.dec_price_venta)	
		else:
			precio=round(float(precio),self.dec_price_venta)
		precio=str(precio)	
		orden_venta=cliente.order_limit_sell(symbol=self.moneda, quantity=str(limite), price=precio)
		self.orden_venta
		return orden_venta	
		
	def cancelar_orden(self,identificacion_orden):
		result = cliente.cancel_order(symbol=self.moneda, orderId=identificacion_orden)
		self.result
		
		return result



BNBEUR=MERCADO('BNBEUR','EUR','BNB')
CHZUSDT=MERCADO("CHZUSDT", "USDT","CHZ")
BTCUSDT=MERCADO("BTCUSDT", "USDT", "BTC")
ETHUSDT=MERCADO("ETHUSDT", "ETH", "USDT")			


def lista_mercados():
	BNBEUR=MERCADO('BNBEUR','EUR','BNB')
	CHZUSDT=MERCADO("CHZUSDT", "USDT","CHZ")
	BTCUSDT=MERCADO("BTCUSDT", "USDT", "BTC")
	ETHUSDT=MERCADO("ETHUSDT", "ETH", "USDT")

	lista_de_mercados=(BNBEUR,CHZUSDT,BTCUSDT,ETHUSDT)
	return lista_de_mercados





#print(BNBEUR.media_ponderada(2))

#print(BNBEUR.maximo)









