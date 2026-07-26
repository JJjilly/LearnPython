import os
import psycopg2
import yfinance as yf
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

supabase: Client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
cursor = psycopg2.connect(os.getenv("DATABASE_URL"))
curs = cursor.cursor(cursor_factory=psycopg2.extras.DictCursor)

curs.execute("SELECT ticker FROM companies")
rows = curs.fetchall()
symbols = [row["ticker"] for row in rows]

for symbol in symbols:
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        if not info or info.get("regularMarketPrice") is None:
            print(f"Delistato o non trovato: {symbol}")
            continue

        last_quote = info.get("regularMarketPrice") or info.get("currentPrice")
        print(f"{symbol}: {last_quote}")

    except Exception as e:
        print(f"Errore su {symbol}: {e}")
        continue

curs.close()
cursor.close()