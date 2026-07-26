from fastapi import FastAPI, Request
import os
import psycopg2
from dotenv import load_dotenv
from supabase import create_client, Client
from psycopg2.extras import DictCursor
from fastapi.templating import Jinja2Templates

load_dotenv()  # va fuori dalla route, si esegue una volta sola

app = FastAPI()

templates = Jinja2Templates(directory="templates")
@app.get("/")
def index(request: Request):
    supabase: Client = create_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_KEY"]
    )
    cursor = psycopg2.connect(os.getenv("DATABASE_URL"))
    curs = cursor.cursor(cursor_factory=psycopg2.extras.DictCursor)
    curs.execute("SELECT ticker, company FROM companies")
    rows = curs.fetchall()
    curs.close()
    cursor.close()
    return templates.TemplateResponse(request=request,name="index.html",context={"ticker": rows})
    return {"tickers": [row["ticker"] for row in rows]}