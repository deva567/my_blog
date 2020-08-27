import logging
from kiteconnect import KiteConnect
from configparser import ConfigParser 
from pprint import pprint
import pdb

  
configur = ConfigParser() 
configur.read('config.ini')
Api_key= configur.get('credentials','Api_key')
Api_secret= configur.get('credentials','Api_secret')
Access_token= configur.get('credentials','Access_token')
print(Api_key)
print(Api_secret)
print(Access_token)

kws = KiteTicker(Api_key, Access_token)


def on_ticks(ws, ticks):
    print(ticks)
    print("\n")
    # pdb.set_trace()


def on_connect(ws, response):
    ws.subscribe([3050241, 177665])
    ws.set_mode(ws.MODE_FULL, [3050241, 177665])


kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.connect()
