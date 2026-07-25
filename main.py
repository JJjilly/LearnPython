import os
from logging import exception

import pytickersymbols
from dotenv import load_dotenv
import yfinance
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

from pycparser.c_ast import If
from pytickersymbols import PyTickerSymbols
from supabase import create_client, Client
import psycopg2
import alpaca_trade_api as tradeapi
import base64
import requests

load_dotenv()
AlpacaAPI = tradeapi.REST('PKFF2W2FF6GN6YAKZKPSZNJV6U', 'BygFhuW5kAZ7eUtrL7ka1sS9LaM7dXMo2fn6q36Zg87x', base_url='https://paper-api.alpaca.markets' )
assets = AlpacaAPI.list_assets()


supabase : Client = create_client(os.environ["supabaseUrl"],os.environ["supabaseKey"])


cursor = psycopg2.connect(os.getenv("DATABASE_URL"))
curs = cursor.cursor()

for asset in assets:
    try:
       if asset.status == 'active'and asset.tradable:
           curs.execute("Insert into companies (company, ticker) VALUES (%s,%s)", (asset.name, asset.symbol))

    except Exception as e:
        print(asset.symbol)
        print(e)

#with cursor.cursor() as curs:
#    curs.execute("Insert into companies (company, ticker) VALUES ('microsoft','MSFT')")
#    curs.execute("Delete From companies")



cursor.commit()
