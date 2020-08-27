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
try: 
	conn=MongoClient("mongodb+srv://Vd4vennam:Vd4vennam@cluster0.ulcey.mongodb.net/TradeTech?retryWrites=true&w=majority")
	db = conn.TradeTech
	# collection = db.APIData
	collection = db.Trial
	print("Connected successfully!!!") 
except Exception as e:   
	print("Could not connect to MongoDB") 
	print(e)

op={81153:{'stock_name': 'BAJFINANCE', 'stock_id': 81153, 'Prop': 1000, 'low': 3510.0, 'high': 3000.0, 'buy': 0, 'sell': 0}, 315393:{'stock_name': 'GRASIM', 'stock_id': 315393, 'Prop': 1000, 'low': 661.65, 'high': 679.45, 'buy': 0, 'sell': 0}, 2911489:{'stock_name': 'BIOCON', 'stock_id': 2911489, 'Prop': 1000, 'low': 385.8, 'high': 394.6, 'buy': 0, 'sell': 0}, 779521:{'stock_name': 'SBIN', 'stock_id': 779521, 'Prop': 1000, 'low': 202.7, 'high': 208.45, 'buy': 0, 'sell': 0}, 2815745:{'stock_name': 'MARUTI', 'stock_id': 2815745, 'Prop': 1000, 'low': 7075.65, 'high': 7175.7, 'buy': 0, 'sell': 0},738561:{'stock_name': 'RELIANCE', 'stock_id': 738561, 'Prop': 1000, 'low': 2078.0, 'high': 2111.3, 'buy': 0, 'sell': 0}, 617473:{'stock_name': 'PEL', 'stock_id': 617473, 'Prop': 1000, 'low': 1400.0, 'high': 1440.0, 'buy': 0, 'sell': 0}, 340481:{'stock_name': 'HDFC', 'stock_id': 340481, 'Prop': 1000, 'low': 1817.05, 'high': 1852.4, 'buy': 0, 'sell': 0},81153:{'stock_name': 'BAJFINANCE', 'stock_id': 81153, 'Prop': 1000, 'low': 3510.0, 'high': 3598.0, 'buy': 0, 'sell': 0}, 315393:{'stock_name': 'GRASIM', 'stock_id': 315393, 'Prop': 1000, 'low': 661.65, 'high': 679.45, 'buy': 0, 'sell': 0}, 2911489:{'stock_name': 'BIOCON', 'stock_id': 2911489, 'Prop': 1000, 'low': 385.8, 'high': 394.6, 'buy': 0, 'sell': 0}}

# collection.insert_one({"load_date_time":datetime.now(),"stock_content":{'stock_name': 'IDEA', 'stock_id': 3677697, 'Prop': 1000}})



# client = pymongo.MongoClient("mongodb+srv://Vd4vennam:<password>@cluster0.ulcey.mongodb.net/<dbname>?retryWrites=true&w=majority")
# db = client.test

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
logger.info('The API credentials read successfully with Access_token')
# print(Api_key)
# print(Api_secret)
# print(Access_token)
Market_stock=pd.read_csv('Market_Stock_Id_List.csv')
logger.info('Reading stock list from csv completed')
stockId=list(Market_stock['stock_id'])
print(stockId)

# def get_login(Api_key, Api_secret): 
#     '''This function will gives Access Token based on Api Parameters'''
#     try:
#         kite = KiteConnect(api_key=Api_key)
#         print("Generate access Token : ", kite.login_url())
#         request_tkn = input("Enter Your Request Token Here : ")
#         print(request_tkn)
#         data = kite.generate_session(request_tkn, api_secret=Api_secret)
#         print(data)
#         logger.info('Requested for new session.')
#         kite.set_access_token(data["access_token"])
#         kws = KiteTicker(Api_key, data["access_token"])
#         print('Access_Token is :: ',data['access_token'])
#         logger.info('Access Token is {}'.format(data['access_token']))
#         return kite,data['access_token']


#     except :
#         print('Token is invalid or has expired.')
#         logger.debug('The flow is in Except block.')
#         logger.error('Token is invalid or has expired.')


# kite,Access_token=get_login(Api_key, Api_secret)
# Access_token="Sdkhe1DJPVs2v9mLA09Bpu81GktHZWkn"
kite = KiteConnect(api_key=Api_key)
kite.set_access_token(Access_token)
# stock_dict={}

 

list_dict=DataFrameToDict.dftodict(Market_stock) # returns the list of dictionary items
logger.info('called Vennam package for dict items')
# print(list_dict)

# for i in list_dict:
#   stock_dict.update(i)
	# print(i)

# for i,j in Market_stock.iterrows():
#   print(i,j)

stock_dict = {str(item['stock_id']):item for item in list_dict}

# print(stock_dict)

# print(list_dict)

# print(stock_dict)



# print(stock_dict[3677697]['low'])
kws = KiteTicker(Api_key, Access_token)


# def buy_stock(name,qnty,last_price):
# 	try:
# 		logger.info(f'The trade {name} id going to buy')
# 		prof=round(0.02* last_price,1)
# 		stopls=round(0.01* last_price,1)
# 		order_id = kite.place_order(tradingsymbol=name,
# 									exchange=kite.EXCHANGE_NSE,
# 									transaction_type=kite.TRANSACTION_TYPE_BUY,
# 									quantity=qnty,
# 									order_type=kite.ORDER_TYPE_SL,
# 									product=kite.PRODUCT_MIS,
# 									variety=kite.VARIETY_REGULAR,
# 									validity=kite.VALIDITY_DAY)
# 									# stoploss=stopls,
# 									# squareoff=prof)
# 									# margins=kite.MARGIN_EQUITY  )
# 		print('order placed',order_id)

# 		logger.info("Order placed. ID is: {}".format(order_id))
# 	except Exception as e:
# 		print(e)
# 		logger.info("Order placement failed: {}".format(e))

# def sell_stock(name,qnty):
#   try:
#     logger.info(f'The trade {name} id going to sell')
#     order_id = kite.place_order(tradingsymbol=name,
#                   exchange=kite.EXCHANGE_NSE,
#                   transaction_type=kite.TRANSACTION_TYPE_SELL,
#                   quantity=qnty,
#                   order_type=kite.ORDER_TYPE_MARKET,
#                   product=kite.PRODUCT_CNC)

#     logger.info("Order sold. ID is: {}".format(order_id))
#   except Exception as e:
#     logger.info("Order selling failed: {}".format(e.message))

# buy_stock('IDFCFIRSTB',1,31)


# def find_one():
# 	# data=collection.find({},{'_id': 0,
# 	# 	"stock_content": 1})
# 	# # l=list(r)
# 	# print(dumps(l))
# 	post = collection.find_one({['stock_content']::int(315393)}) 
# 	print(post)
# 	# for i in data:
# 	# 	print(i['stock_content'])
# 	# 	print('\n')


# find_one()


count=0
final_doct=[]
dictionary={}
# sample={str(i):{} for i in stockId}
# print(sample)
def on_ticks(ws, ticks):
	print(ticks)
    
	for item in ticks:
		global count,final_doct
		print(item['instrument_token'])
		print('high',item['ohlc']['high'])
		print('low',item['ohlc']['low'])
		print('last price',item['last_price'])
		maximum_ins=item['ohlc']['high']
		minimum_ins=item['ohlc']['low']
		lp=item['last_price']
		# data=collection.find({},{'_id': 0,
		# "stock_content": 1})
		for key in list(stock_dict):
			if key==str(item['instrument_token']):
				print('inside of sample docs')
				count=count+1
				stock_dict[key].update({'low':item['ohlc']['low'],'high':item['ohlc']['high'],'buy':0,'sell':0})
				if count==8:
					tag_var=date.today()
					collection.insert_one({'tag':str(tag_var),'content':stock_dict})
		# print(sample)


		# dictionary.update(item['instrument_token']:{'low':item['ohlc']['low'],'high':item['ohlc']['high'],'buy':0,'sell':0})
		# print(dictionary)
#----------------------------------------------------------------------------#
		# if op[item['instrument_token']]['buy']==0 and lp>op[item['instrument_token']]['high']:
		# 	print(f"{op[item['instrument_token']]['stock_name']}--high--{op[item['instrument_token']]['high']}--LP--{lp} --{op[item['instrument_token']]['stock_id']}  is in ORB---Maximum-- {datetime.now()}")
		# 	op[item['instrument_token']]['buy']=1
#-------------------------------------------------------------------------------#


		# for i in stock_dict.keys():
		# 	if i==str(item['instrument_token']):
		# 		print(i)# stock_dict[i].append({'low':'22','high':'33'})
		# 		stock_dict[i].update({'low':item['ohlc']['low'],'high':item['ohlc']['high'],'buy':0,'sell':0})
		# 		count=count+1
		# 		final_doct.append(stock_dict[i].copy())
		# 		print("count:  ", count)
		# 		if count>8:
		# 			collection.insert_one(final_doct)
		# 		# 	# sys.exit(0)
		# 		# 	# validation(count)
		# 		# 	print('inserted docs')
		# 		# elif count==9:
		# 		# 	sys.exit(0)


		# for stock_name in data:
		# 	if stock_name['stock_content']['stock_id']==item['instrument_token']:
		# 		if item['last_price']>stock_name['stock_content']['high']:
		# 		  # stock_dict[i].update({'low':item['ohlc']['low'],'high':item['ohlc']['high']})
		# 		  # print(stock_name['stock_content'].update({'buy':'yes'}))
		# 		  # collection.insert_one({"load_date_time":datetime.now(),"stock_content":stock_name})
		# 		  # print('data updated in mongo')
		# 		  print(f"{stock_name['stock_content']['stock_name']}--{stock_name['stock_content']['high']}--{item['last_price']} --{stock_name['stock_content']['stock_id']}is in ORB---Maximum-- {datetime.now()}")
		# 		  # print('Maximum')
		# 		  post = collection.find_one({"_id":mongo_id}) 
		# 		  stock_name['buy'] = 1

		# 		  collection.update_one({'stock_id':stock_name['stock_content']['stock_id']}, {"$set": stock_name}, upsert=False)

		# 		  logger.info(f"{stock_name['stock_content']['stock_name']}--{stock_name['stock_content']['high']}--LP is :{item['last_price']} --{stock_name['stock_content']['stock_id']}is in ORB---Maximum-- {datetime.now()}")
		# 		  print('\n')
		# 		  # print(item['instrument_token'])
		# 		elif item['last_price']<stock_name['stock_content']['low']:
		# 		  print(f"{stock_name['stock_content']['stock_name']}--{stock_name['stock_content']['low']}--{item['last_price']}--{stock_name['stock_content']['stock_id']}  is in ORB --Minimum ----{datetime.now()} ")
		# 		  # print('Minimum')
		# 		  logger.info(f"{stock_name['stock_content']['stock_name']}--{stock_name['stock_content']['low']}-- LP is :{item['last_price']}--{stock_name['stock_content']['stock_id']}  is in ORB --Minimum ----{datetime.now()} ")
		# 		  print('\n')
				  # print(item['instrument_token'])

		# for i in op:
		# 	if i['stock_id']==item['instrument_token'] :
		# 		if item['last_price']>i['high'] and i['buy']==0:
		# 			i['buy']=1

			
		# 			print(f"{i['stock_name']}--high--{i['high']}--LP--{item['last_price']} --{i['stock_id']}  is in ORB---Maximum-- {datetime.now()}")
		# 	  # print('Maximum')

		# 			logger.info(f"{i['stock_name']}--high--{i['high']}--LP--{item['last_price']} --{i['stock_id']}is in ORB---Maximum-- {datetime.now()}")

		# 		elif item['last_price']<i['low'] and i['sell']==0:
		# 			i.update({'sell':1})
			
		# 			print(f"{i['stock_name']}--low--{i['low']}--LP--{item['last_price']} --{i['stock_id']}  is in ORB---Minimum-- {datetime.now()}")
		# 	  # print('Maximum')

		# 			logger.info(f"{i['stock_name']}--low--{i['low']}--LP--{item['last_price']} --{i['stock_id']}is in ORB---Minimum-- {datetime.now()}")








		# if item['last_price']>maximum_ins:
		#   print('Maximum')
		#   print(item['instrument_token'])

		#   # buy_stock('HDFC',1,lp)
		# if item['last_price']<minimum_ins:
		#   # sell_stock('IDEA',1,lp)
		#   print('Minimum')
		#   print(item['instrument_token'])

 




	# print("\n")
	# pdb.set_trace()


def on_connect(ws, response):
	logger.info('The flow is in subscribe function')
	ws.subscribe(stockId)
	ws.set_mode(ws.MODE_QUOTE, stockId)


kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.connect()

# print(stock_dict)
# print(final_doct)

# for i in op:
# 	# print(i)
# 	print('\n')
# 	if i['stock_id']==779521 and i['buy']==0:
# 		print(i['buy'])
# 		i['buy']:'XXX'
# 		print(i)


# print(op)


# if op['stock_id']==779521 and op['buy']==0:
# 	print(i['buy'])
# 	i['buy']:'XXX'
# 	print(i)


# if  op[81153]['buy']==0 and lp>op[81153]['high']:
# 			print(f"{op[81153]['stock_name']}--high--{op[81153]['high']}--LP--{lp} --{op[81153]['stock_id']}  is in ORB---Maximum-- {datetime.now()}")
# 			op[81153]['buy']=1

# print(type(op))

# print(op[81153])

# print(type({123:{'name':'dev'}}))


# print(stockId)

# post = collection.find_one({"tag":'1234'})
# print(post['content']) 
