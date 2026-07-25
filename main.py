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
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
import base64
import requests

load_dotenv()

supabase : Client = create_client(os.environ["supabaseUrl"],os.environ["supabaseKey"])
alpaca = TradingClient(
    os.environ["ALPACA_KEY"],
    os.environ["ALPACA_SECRET"],
    paper=True
)

assets = alpaca.get_all_assets()

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
#Ho aggiunto ON CONFLICT (ticker) DO NOTHING nell'INSERT — così se un ticker esiste già non da errore ma lo salta, evitando duplicati.



cursor.commit()
