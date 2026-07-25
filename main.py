import os
from dotenv import load_dotenv
import yfinance
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from pytickersymbols import PyTickerSymbols
from supabase import create_client, Client
import psycopg2
import alpaca_trade_api as tradeapi


load_dotenv()
AlpacaAPI = tradeapi.REST('PKFF2W2FF6GN6YAKZKPSZNJV6U', 'BygFhuW5kAZ7eUtrL7ka1sS9LaM7dXMo2fn6q36Zg87x', base_url='https://paper-api.alpaca.markets' )
asset = AlpacaAPI.list_assets()

for asset in asset:
    print(asset)

supabase : Client = create_client(os.environ["supabaseUrl"],os.environ["supabaseKey"])


cursor = psycopg2.connect(os.getenv("DATABASE_URL"))

with cursor.cursor() as curs:
    curs.execute("""Insert into companies (company, ticker) VALUES ('microsoft','MSFT')""")

cursor.commit()
