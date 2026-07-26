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
import yfinance as yf
import main

load_dotenv()
#Setup connection with supabase db
supabase: Client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
#setup connection with alpaca broker
alpaca = TradingClient(
    os.environ.get("ALPACA_KEY", ""),
    os.environ.get("ALPACA_SECRET", ""),
    paper=True
)
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
    try:
        ticker = yf.Ticker(ticker)
        info = ticker.info
        # Verifica che il ticker sia valido prima di usarlo
        if not info or info.get('regularMarketPrice') is None:
            print(f"Ticker non valido o delistato: {ticker}")
            continue
        last_quote = info.last_price
    except Exception as e:
        print(f"Errore su {ticker}: {e}")
        continue




