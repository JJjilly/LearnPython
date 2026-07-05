import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

  # Press Ctrl+F8 to toggle the breakpoint.

    # Use a breakpoint in the code line below to debug your script.
##acronimi azioni
def get_universe():
    df = pd.read_csv("backend/data/europa_tickers.csv")
    return df["ticker"].tolist()

tickers = get_universe()
##fino a quale giorno
end_date = datetime.today()
startdate = end_date - timedelta(days=1)

##chiusure prezzi

yf.config.debug.logging = True
close_df = pd.DataFrame()

for ticker in tickers:
    data = yf.download(ticker, start = startdate, end = end_date)
    close_df[ticker] = data['Close']

print(end_date)
print(close_df)

##name = 'halal program' # declaring without datatype makes automatically it decide if string or any other datatype
##makepippo = 123454 ##capisce di che datatype si tratta
##conc = 'basically'
##listpy = ['one', 'two', 'three', 'four', 'five'] #array
##uniquepy = {1,2,3,4,5} #set di dati univoci
##structc = {'bob':2, 'mio' : 3} #coordinate struct
##age : int = 10  #declaring explicitly integer datatype
##def func():
##  print(name)
##   print(conc)
##  print(makepippo + 100)
##func()

# Press the green button in the gutter to run the script.

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
