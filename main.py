import os
import base64
import requests
import psycopg2
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pytickersymbols import PyTickerSymbols
from supabase import create_client, Client
from alpaca.trading.client import TradingClient

load_dotenv()

supabase: Client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
alpaca = TradingClient(
    os.environ.get("ALPACA_KEY", ""),
    os.environ.get("ALPACA_SECRET", ""),
    paper=True
)

assets = alpaca.get_all_assets()

cursor = psycopg2.connect(os.getenv("DATABASE_URL"))
curs = cursor.cursor()

for asset in assets:
    try:
        if asset.status == 'active' and asset.tradable:
            curs.execute(
                "INSERT INTO companies (company, ticker) VALUES (%s, %s) ON CONFLICT (ticker) DO NOTHING",
                (asset.name, asset.symbol)
            )
    except Exception as e:
        print(asset.symbol)
        print(e)

cursor.commit()
curs.close()
cursor.close()