import os
import base64
import requests
import psycopg2
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from psycopg2.extras import DictCursor
from pytickersymbols import PyTickerSymbols
from supabase import create_client, Client
from alpaca.trading.client import TradingClient
import alpaca_trade_api as tradeapi
import yfinance as yf
import main
from alpaca_trade_api import TimeFrame

load_dotenv()
#Setup connection with supabase db
supabase: Client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
#setup connection with alpaca broker
alpaca = TradingClient(
    os.environ.get("ALPACA_KEY", ""),
    os.environ.get("ALPACA_SECRET", ""),
    paper=True
)
api = tradeapi.REST(os.environ.get("ALPACA_KEY", ""),os.environ.get("ALPACA_SECRET", ""),base_url=os.environ.get("ALPACA_URL"))
assets = alpaca.get_all_assets()
#Connect to supabase using postgre so You can use cursor, otherwise you use superbase client
cursor = psycopg2.connect(os.getenv("DATABASE_URL"))
#Declare cursor
# Corretto — passa DictCursor quando crei il cursore
curs = cursor.cursor(cursor_factory=psycopg2.extras.DictCursor)



curs.execute("SELECT ticker FROM companies")
rows = curs.fetchall()

symbols = [row["ticker"] for row in rows]

for ticker in symbols:
    stock = yf.Ticker(ticker)
    data = stock.history()
    info = stock.fast_info
    last_quote = info.last_price
    print(ticker, last_quote)




