# https://api.telegram.org/bot1266300791:AAHLFI-KGcjEkIZ1-qJBMa86w2LnriRkmgg/getupdates
import logging 
from configparser import ConfigParser 
import requests
from pymongo import MongoClient 
from datetime import datetime
configur = ConfigParser() 
configur.read('config.ini')
connectionString= configur.get('MongoDB','connectionString')

try: 
    conn=MongoClient(connectionString)
    db = conn.TradeTech
    collection1 = db.ChatHistory
    collection=db.AlertData
    print("Connected successfully!!!") 
except Exception as e:   
    print("Could not connect to MongoDB") 
    print(e)





logging.basicConfig(filename="monitoring.log", 
                    format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    filemode='a',
                    datefmt = '%d/%m/%Y %I:%M:%S %p')
logger=logging.getLogger() 
  
logger.setLevel(logging.DEBUG)




logger.info('started Telegram Vennam_Bot')
configur = ConfigParser() 
configur.read('config.ini')
Base_url= configur.get('telegram','base_url')
# print(Base_url)

def tel_bot(message):

	Final_req=Base_url+message

	response=requests.get(Final_req)

	collection.insert_one({"load_date_time":datetime.now(),"Vennam_Bot":'Testing from Vennam_Bot for HIstory Check'})

	collection1.insert_one({"load_date_time":datetime.now(),"Vennam_Bot":response.json()})

	print(response.json())



# Api_secret= configur.get('credentials','Api_secret')