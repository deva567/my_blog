import logging
from kiteconnect import KiteConnect
from configparser import ConfigParser 
from kiteconnect import KiteTicker
from pprint import pprint
import pdb
import pandas as pd
from vennam import DataFrameToDict
from pymongo import MongoClient 
from datetime import datetime
import sys
from bson.json_util import dumps
from datetime import date
from Telegram_Bot import tel_bot
import time

logging.basicConfig(filename="monitoring.log", 
					format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s', 
					filemode='a',
					datefmt = '%d/%m/%Y %I:%M:%S %p' )
logger=logging.getLogger() 

logger.setLevel(logging.DEBUG)

logger.info('started The main script for getting Live Data')
configur = ConfigParser() 
configur.read('config.ini')
Api_key= configur.get('credentials','Api_key')
Api_secret= configur.get('credentials','Api_secret')
Access_token= configur.get('credentials','Access_token')
connectionString= configur.get('MongoDB','connectionString')
logger.info('The API credentials read successfully with Access_token')

kite = KiteConnect(api_key=Api_key)
kite.set_access_token(Access_token)
kws = KiteTicker(Api_key, Access_token)


#----holdings-----------
# print('holdings:::::')
# print(kite.holdings())
#-----------------orders------------
# print('The Orders are:::::')

# temp=kite.orders()

# orderList=temp[0]
# # pprint(orderList)
# pprint(temp)
# print('tradingsymbol::::::',orderList['tradingsymbol'])

# print('instrument_token:::::' ,orderList['instrument_token'])

# print('filled_quantity:::::',orderList['filled_quantity'])

# print('quantity::::::',orderList['quantity'])
#------------------trades--------------

# print('\n')

# trades=kite.trades()
# pprint(trades[0])
# print(trades[0]['tradingsymbol'])

#----------------------


# try: 
# 	conn=MongoClient(connectionString)
# 	db = conn.TradeTech
# 	# collection = db.APIData
# 	collection = db.Trial
# 	collection1=db.Tomorrow
# 	print("Connected successfully from order scripts") 
# except Exception as e:   
# 	print("Could not connect to MongoDB") 
# 	print(e)



# Market_stock=pd.read_csv('Market_Stock_Id_List.csv')
# logger.info('Reading stock list from csv completed')
# stockId=list(Market_stock['stock_id'])

# tag_var=str(date.today())
# post1 = collection.find_one({"tag":tag_var})
# post=post1['content']
# # pprint(post)

# def buy_stock(name,qnty,last_price):
# 	try:
# 		logger.info(f'The trade {name} id going to buy')
# 		prof=round(0.02* last_price,1)
# 		print('profit:::::::>>'mprof)
# 		stopls=round(0.01* last_price,1) 
# 		print('stoploss:::::>>',stopls)

# 		print('\n')
# 		# print(last_price+0.1)
# 		# order_id=12345
# 		order_id = kite.place_order(tradingsymbol=name,
# 									exchange=kite.EXCHANGE_NSE,
# 									transaction_type=kite.TRANSACTION_TYPE_BUY,
# 									quantity=qnty,
# 									order_type=kite.ORDER_TYPE_SL,
# 									product=kite.PRODUCT_MIS,
# 									variety=kite.VARIETY_REGULAR,
# 									validity=kite.VALIDITY_DAY,
# 									stoploss=stopls,
# 									price= last_price,
# 									squareoff=prof,
# 									trigger_price=last_price
# 									)
# 									# squareoff=prof)
# 									# margins=kite.MARGIN_EQUITY  )
# 		print('order placed',order_id)
# 		tel_bot(f'order Placed {order_id}')

# 		logger.info("Order placed. ID is: {}".format(order_id))
# 	except Exception as e:
# 		print(e)
# 		logger.info("Order placement failed: {}".format(e))
# 		tel_bot(f'order placing failed due to ::{e}')

def sell_stock(name,qnty,trigger_price):
	try:
		logger.info(f'The trade {name} id going to sell')
		order_id = kite.place_order(tradingsymbol=name,
		              exchange=kite.EXCHANGE_NSE,
		              transaction_type=kite.TRANSACTION_TYPE_SELL,
		              quantity=qnty,
		              order_type=kite.ORDER_TYPE_SLM,
		              product=kite.PRODUCT_MIS,
		              variety=kite.VARIETY_REGULAR,
					  validity=kite.VALIDITY_DAY,
					  trigger_price=trigger_price)


		tel_bot(f'order sold and order ID : {order_id}')
		print('order sold :::::',order_id)
		logger.info("Order sold. ID is: {}".format(order_id))
	except Exception as e:
		print(e)
		logger.info("Order selling failed: {}".format(e))
		tel_bot(f'order selling failed due to ::{e}')

# sell_stock(trades[0]['tradingsymbol'],1,215.30)#-----this is for sell order
# def on_ticks(ws, ticks):
# 	for item in ticks:
# 		print(item['instrument_token'])
# 		# print('high',item['ohlc']['high'])
# 		# print('low',item['ohlc']['low'])
# 		print('last price',item['last_price'])
# 		maximum_ins=item['ohlc']['high']
# 		minimum_ins=item['ohlc']['low']
# 		lp=item['last_price']
# 		# print('.......')
# 		#post[str(item['instrument_token'])]['high']------<<<<<<
# 		if post[str(item['instrument_token'])]['buy']==0 and lp>200:
# 			logger.info('Inside Of Maximum')
# 			buy_stock(post[str(item['instrument_token'])]['stock_name'],1,lp)# buy stock function---------
# 			tel_bot(f"{post[str(item['instrument_token'])]['stock_name']} has been purchased now through scripts..")

# 			print('----------------quantity-------------')
# 			qnty=int(post[str(item['instrument_token'])]['Prop']//lp)
# 			logger.info(f"{post[str(item['instrument_token'])]['stock_id']}--{post[str(item['instrument_token'])]['stock_name']}--qnty--{qnty}")
# 			print('qnty------->',qnty)
# 			amount_spent=int(qnty*lp)
# 			logger.info(f"{post[str(item['instrument_token'])]['stock_id']}--{post[str(item['instrument_token'])]['stock_name']}--qnty--{qnty}--amount_spent--{amount_spent}")

# 			print('amount_spent------>',amount_spent)

# 			rem_amount=post[str(item['instrument_token'])]['Prop']-amount_spent
# 			logger.info(f"{post[str(item['instrument_token'])]['stock_id']}--{post[str(item['instrument_token'])]['stock_name']}--qnty--{qnty}--amount_spent--{amount_spent}--rem_amount--{rem_amount}")

# 			print('remainig------>',rem_amount)
# 			print('inside maximum')
# 			print('\n')
# 			print('--------------------------------------')

# 			print(f"{post[str(item['instrument_token'])]['stock_name']}--high--{post[str(item['instrument_token'])]['high']}--LP--{lp} --{post[str(item['instrument_token'])]['stock_id']}  is in ORB---Maximum-- {datetime.now()}")
# 			logger.info(f"{post[str(item['instrument_token'])]['stock_name']}--high--{post[str(item['instrument_token'])]['high']}--LP--{lp} --{post[str(item['instrument_token'])]['stock_id']}  is in ORB---Maximum-- {datetime.now()}")
# 			post[str(item['instrument_token'])]['buy']=1
# 			post[str(item['instrument_token'])]['Prop']=rem_amount
# 			print('after update')
# 			doc = collection.find_one_and_update(
# 											    {"tag" :tag_var},
# 											    {"$set":
# 											        {"content": post}
# 											    },upsert=True
# 											)
# 			time.sleep(8)

# 		if post[str(item['instrument_token'])]['sell']==0 and lp<post[str(item['instrument_token'])]['low']:
# 			logger.info('Inside of Minimum')
# 			sell_stock(post[str(item['instrument_token'])]['stock_name'],1)
# 			tel_bot(f"{post[str(item['instrument_token'])]['stock_name']} has been sold now through scripts..")

# 			print('----------------quantity-------------')
# 			# qnty=int(post[str(item['instrument_token'])]['Prop']//lp)
# 			qnty=int(20)
# 			logger.info(f"{post[str(item['instrument_token'])]['stock_id']}--{post[str(item['instrument_token'])]['stock_name']}--qnty--{qnty}")
# 			print('qnty------->',qnty)
# 			amount_spent=int(qnty*lp)
# 			logger.info(f"{post[str(item['instrument_token'])]['stock_id']}--{post[str(item['instrument_token'])]['stock_name']}--qnty--{qnty}--amount_spent--{amount_spent}")

# 			print('amount_spent------>',amount_spent)

# 			rem_amount=post[str(item['instrument_token'])]['Prop']+amount_spent
# 			logger.info(f"{post[str(item['instrument_token'])]['stock_id']}--{post[str(item['instrument_token'])]['stock_name']}--qnty--{qnty}--amount_spent--{amount_spent}--rem_amount--{rem_amount}")

# 			print('remainig------>',rem_amount)
# 			print('inside minimum')
# 			print('\n')


# 			print(f"{post[str(item['instrument_token'])]['stock_name']}--low--{post[str(item['instrument_token'])]['low']}--LP--{lp} --{post[str(item['instrument_token'])]['stock_id']}  is in ORB---Minimum-- {datetime.now()}")
# 			logger.info(f"{post[str(item['instrument_token'])]['stock_name']}--low--{post[str(item['instrument_token'])]['low']}--LP--{lp} --{post[str(item['instrument_token'])]['stock_id']}  is in ORB---Minimum-- {datetime.now()}")
# 			post[str(item['instrument_token'])]['sell']=1
# 			post[str(item['instrument_token'])]['Prop']=rem_amount
# 			doc = collection.find_one_and_update(
# 											    {"tag" :tag_var},
# 											    {"$set":
# 											        {"content": post}
# 											    },upsert=True
# 											)



# def on_connect(ws, response):
# 	logger.info('The flow is in subscribe function')
# 	ws.subscribe([779521])
# 	ws.set_mode(ws.MODE_QUOTE, [779521])


# kws.on_ticks = on_ticks
# kws.on_connect = on_connect
# kws.connect()


# def futureData():
# 	future=post
# 	for i in future:
# 		# print(future[i])
# 		future[i]['low']=0
# 		future[i]['high']=0
# 		future[i]['buy']=0
# 		future[i]['sell']=0

# 	# print(future)
# 	tag_var=date.today()
# 	collection1.insert_one({'tag':str(tag_var),'content':future})
# 	logger.info('Data has been uploaded to MongoDB Cluster for Future')


# futureData()

# buy_stock('SBIN',1,213.60)
