from binance.client import Client
import usuario1 
from binance import ThreadedDepthCacheManager
from binance import BinanceSocketManager
from binance import DepthCacheManager
from binance import *
import time
from colorama import init, Fore, Back, Style


cliente=Client(usuario1.api_key,usuario1.secret_key)
eth_balance = cliente.get_asset_balance(asset='ETH')
print(eth_balance)
moneda="ETHEUR"
symbolTicker = 'ETHEUR'
symbolPrice = 0
ma50 = 0
auxPrice = 0.0

def orderStatus(orderToCkeck):
    try:
        status = cliente.get_order(
            symbol = symbolTicker,
            orderId = orderToCkeck.get('orderId')
        )
        return status.get('status')
    except Exception as e:
        print(e)
        return 7

def _tendencia_ma50_4hs_15minCandles_():
    x = []
    y = []
    sum = 0
    ma50_i = 0

    time.sleep(1)

    resp = False

    klines = cliente.get_historical_klines(symbolTicker, Client.KLINE_INTERVAL_15MINUTE, "18 hour ago UTC")

    if (len(klines) != 72):
        return False
    for i in range(56,72):
        for j in range(i-50,i):
            sum = sum + float(klines[j][4])
        ma50_i = round(sum / 50,8)
        sum = 0
        x.append(i)
        y.append(float(ma50_i))

    modelo = np.polyfit(x, y, 1)

    if (modelo[0]>0):
        resp = True

    return resp

def _ma50_():
    ma50_local = 0
    sum = 0

    klines = cliente.get_historical_klines(symbolTicker, Client.KLINE_INTERVAL_15MINUTE, "15 hour ago UTC")

    if (len(klines) == 60):

        for i in range(10,60):
            sum = sum + float(klines[i][4])

        ma50_local = sum / 50

    return ma50_local



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

orden_compra=False
orden_venta=False
it=0
while it<=100:
	time.sleep(2)
	profundidad=cliente.get_order_book(symbol=moneda)
	compras=0
	ventas=0
	for i in profundidad["bids"]:
		compras=compras+ float(i[1])
	print(compras)	 
	
	for i in profundidad["asks"]:
		ventas=ventas+ float(i[1])
	print(ventas)	
	porcentaje_compras=(100*compras/(compras+ventas))-50
	porcentaje_ventas=(100*ventas/(compras+ventas))-50

	if porcentaje_compras>5:
		posibilidad_compra+=1
		posibilidad_venta=0
		orden_venta=False
	elif porcentaje_ventas>5:
		posibilidad_venta+=1
		posibilidad_compra=0
		orden_compra=False	
	it+=1	
	if posibilidad_compra==5:
		orden_compra=True
	elif porcentaje_ventas==5:
		orden_venta=True	


	sum = 0

    # BEGIN GET PRICE
	try:
		list_of_tickers = cliente.get_all_tickers()
	except Exception as e:
	with open("ADABTC_scalper.txt", "a") as myfile:
	    myfile.write(str(datetime.datetime.now()) +" - an exception occured - {}".format(e)+ " Oops 1 ! \n")
	cliente = Client(config.API_KEY, config.API_SECRET, tld='com')
	continue

    for tick_2 in list_of_tickers:
        if tick_2['symbol'] == symbolTicker:
            symbolPrice = float(tick_2['price'])
    # END GET PRICE

    ma50 = _ma50_()
    if (ma50 == 0): continue

    print("********** " + symbolTicker + " **********")
    print(" ActualMA50: "  + str(round(ma50,8)))
    print("ActualPrice: " + str(round(symbolPrice,8)))
    print(" PriceToBuy: "  + str(round(ma50*0.99,8)))
    print("----------------------")

    try:
        orders = cliente.get_open_orders(symbol=symbolTicker)
    except Exception as e:
        print(e)
        cliente = Client(config.API_KEY, config.API_SECRET, tld='com')
        continue

    if (len(orders) != 0):
        print("There is Open Orders")
        time.sleep(20)
        continue
    if (not _tendencia_ma50_4hs_15minCandles_()):
        print("Decreasing")
        time.sleep(20)
        continue
    else:
        print("Creasing")

    if ( symbolPrice < ma50*0.99 ):
        print("DINAMIC_BUY")

        try:

            buyOrder = cliente.create_order(
                        symbol=symbolTicker,
                        side='BUY',
                        type='STOP_LOSS_LIMIT',
                        quantity=400,
                        price='{:.8f}'.format(round(symbolPrice*1.0055,8)),
                        stopPrice='{:.8f}'.format(round(symbolPrice*1.005,8)),
                        timeInForce='GTC')

            auxPrice = symbolPrice
            time.sleep(3)
            while orderStatus(buyOrder)=='NEW':

                # BEGIN GET PRICE
                try:
                    list_of_tickers = cliente.get_all_tickers()
                except Exception as e:
                    with open("ADABTC_scalper.txt", "a") as myfile:
                        myfile.write(str(datetime.datetime.now()) +" - an exception occured - {}".format(e)+ " Oops 2 ! \n")
                    cliente = Client(config.API_KEY, config.API_SECRET, tld='com')
                    continue

                for tick_2 in list_of_tickers:
                    if tick_2['symbol'] == symbolTicker:
                        symbolPrice = float(tick_2['price'])
                # END GET PRICE

                if (symbolPrice < auxPrice):

                    try:
                        result = cliente.cancel_order(
                            symbol=symbolTicker,
                            orderId=buyOrder.get('orderId'))

                        time.sleep(3)
                    except Exception as e:
                        with open("ADABTC_scalper.txt", "a") as myfile:
                            myfile.write(str(datetime.datetime.now()) +" - an exception occured - {}".format(e)+ "Error Canceling Oops 4 ! \n")
                        break


                    buyOrder = cliente.create_order(
                                symbol=symbolTicker,
                                side='BUY',
                                type='STOP_LOSS_LIMIT',
                                quantity=400,
                                price='{:.8f}'.format(round(symbolPrice*1.0055,8)),
                                stopPrice='{:.8f}'.format(round(symbolPrice*1.005,8)),
                                timeInForce='GTC')
                    auxPrice = symbolPrice
                    time.sleep(1)

            time.sleep(10)

            orderOCO = cliente.order_oco_sell(
                        symbol = symbolTicker,
                        quantity = 400,
                        price = '{:.8f}'.format(round(float(symbolPrice)*1.02,8)),
                        stopPrice = '{:.8f}'.format(round(float(symbolPrice)*0.992,8)),
                        stopLimitPrice ='{:.8f}'.format(round(float(symbolPrice)*0.99,8)),
                        stopLimitTimeInForce = 'GTC'
                    )

            time.sleep(20)

        except Exception as e:
            with open("ADABTC_scalper.txt", "a") as myfile:
                myfile.write(str(datetime.datetime.now()) +" - an exception occured - {}".format(e)+ " Oops 3 ! \n")
            client = Client(config.API_KEY, config.API_SECRET, tld='com')
            print(e)
            orders = cliente.get_open_orders(symbol=symbolTicker)
            if (len(orders)>0):
                result = cliente.cancel_order(
                    symbol=symbolTicker,
                    orderId=orders[0].get('orderId'))


            continue


