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

tag_var=str(date.today())

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



try: 
	conn=MongoClient(connectionString)
	db = conn.TradeTech
	# collection = db.APIData
	collection = db.Trial
	collection1=db.Tomorrow
	print("Connected successfully!!!") 
except Exception as e:   
	print("Could not connect to MongoDB") 
	print(e)



Market_stock=pd.read_csv('Market_Stock_Id_List.csv')
logger.info('Reading stock list from csv completed')
stockId=list(Market_stock['stock_id'])
 

list_dict=DataFrameToDict.dftodict(Market_stock) # returns the list of dictionary items
logger.info('called Vennam package for dict items')

stock_dict = {str(item['stock_id']):item for item in list_dict}# This is for csv data
#-------------------------Logic for pulling yesterday's prop-----------
# post1 = collection.find_one({"tag":tag_var})
# stock_dict=post1['content']
#-------------------------------------------------
count=0
def on_ticks(ws, ticks):
	print(ticks)
    
	for item in ticks:
		global count
		print(item['instrument_token'])
		print('high',item['ohlc']['high'])
		print('low',item['ohlc']['low'])
		print('last price',item['last_price'])
		maximum_ins=item['ohlc']['high']
		minimum_ins=item['ohlc']['low']
		lp=item['last_price']
		for key in list(stock_dict):
			if key==str(item['instrument_token']):
				print('inside of sample docs')
				count=count+1
				stock_dict[key].update({'low':item['ohlc']['low'],'high':item['ohlc']['high'],'buy':0,'sell':0})
				if count==len(stockId):
					tag_var=date.today()
					collection.insert_one({'tag':str(tag_var),'content':stock_dict})
					tel_bot(f'The Document has been uploaded to MongoDB Cluster')
					logger.info('The Document has been uploaded to MongoDB Cluster')




def on_connect(ws, response):
	logger.info('The flow is in subscribe function')
	ws.subscribe(stockId)
	ws.set_mode(ws.MODE_QUOTE, stockId)


kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.connect()