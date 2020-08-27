from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import pandas as pd
import logging
from configparser import ConfigParser 
logging.basicConfig(filename="monitoring.log", 
                    format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    filemode='a',
                    datefmt = '%d/%m/%Y %I:%M:%S %p' )
logger=logging.getLogger() 
  
logger.setLevel(logging.DEBUG) 
configur = ConfigParser() 
configur.read('config.ini')
logger.info('Just Read config file.')
Api_key= configur.get('credentials','Api_key')
Api_secret= configur.get('credentials','Api_secret')
print(Api_key)
print(Api_secret)
logger.info('API credentials reading completed .')
logger.info(f'api_key : {Api_key}')
logger.info(f'Api_secret : {Api_secret}')

def get_login(Api_key, Api_secret): 
    '''This function will gives Access Token based on Api Parameters'''
    try:
        kite = KiteConnect(api_key=Api_key)
        print("Generate access Token : ", kite.login_url())
        request_tkn = input("Enter Your Request Token Here : ")
        print(request_tkn)
        data = kite.generate_session(request_tkn, api_secret=Api_secret)
        print(data)
        logger.info('Requested for new session.')
        kite.set_access_token(data["access_token"])
        kws = KiteTicker(Api_key, data["access_token"])
        print('Access_Token is :: ',data['access_token'])
        logger.info('Access Token is {}'.format(data['access_token']))


    except :
        print('Token is invalid or has expired.')
        logger.debug('The flow is in Except block.')
        logger.error('Token is invalid or has expired.')


get_login(Api_key, Api_secret)