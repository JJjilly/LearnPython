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
import stockPrices
#*function to populate database*#

def inserisci_assets(assets, curs):
    nuovi = 0
    errori = 0
    totale = 0

    for asset in assets:
        try:
            if asset.status == 'active' and asset.tradable:
                totale += 1
                curs.execute(
                    """
                    INSERT INTO companies (company, ticker) 
                    VALUES (%s, %s) 
                    ON CONFLICT (ticker) DO NOTHING
                    """,
                    (asset.name, asset.symbol)
                )
                # rowcount = 1 se inserito, 0 se già esisteva
                if curs.rowcount > 0:
                    nuovi += 1

        except Exception as e:
            errori += 1
            print(asset.symbol, e)

    return nuovi, totale, errori

load_dotenv()
#Setup connection with supabase db
supabase: Client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
#setup connection with alpaca broker
alpaca = TradingClient(
    os.environ.get("ALPACA_KEY", ""),
    os.environ.get("ALPACA_SECRET", ""),
    paper=True
)
#get all asset from alpaca
assets = alpaca.get_all_assets()
#Connect to supabase using postgre so You can use cursor, otherwise you use superbase client
cursor = psycopg2.connect(os.getenv("DATABASE_URL"))
#Declare cursor
# Corretto — passa DictCursor quando crei il cursore
curs = cursor.cursor(cursor_factory=psycopg2.extras.DictCursor)

#Call function to populate database
curs.execute("SELECT ticker FROM companies")
rows = curs.fetchall()

symbols = [row["ticker"] for row in rows]

inserisci_assets(assets, curs)
nuovi, totale, errori = inserisci_assets(assets, curs)
supabase.table("workflow_logs").insert({
    "nuovi":   nuovi,
    "totale":  totale,
    "errori":  errori,
    "note":    f"Completato — {nuovi} nuovi su {totale} analizzati"
}).execute()

print(f"✅ Completato: {nuovi} nuovi, {totale} totali, {errori} errori")
#commit chagnes to db
cursor.commit()
#Close cursor
curs.close()
cursor.close()