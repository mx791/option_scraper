import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import os
import boto3

print("Connection to S3")
s3 = boto3.client('s3')
print("Connected")

all_symbols = [
 'AAL', 'AAPL', 'ACB', 'AC.PA', 'ADM', 'AIR.PA', 'AMZN', 'ASHR', 'ATVI', 'BAC', 'BBBYQ', 'BITO', 'C', 'DISH', 'DM', 'EBAY', 'EFA', 'ESI.PA', 'ET', 'EWZ', 'F', 'FXI', 'GM', 'GOOGL', 'HYG', 'IT', 'INVZ', 'IWM', 'JNJ', 'KVUE', 'LUMN', 'MCD', 'META', 'MRNA', 'MULN', 'NFLX', 'NKLA', 'NU', 'NVDA', 'PBR', 'PINS', 'QQQ', 'RIG', 'SNAP', 'SNDL', 'SPY', 'TLT', 'TSLA', 'VALE', 'WAVE.PA', 'XELA', 'XLF', '^SPX', '^VIX'
]

BUCKET_NAME = "791-options-data"

def get_symbol_data(symbol):
    ticker = yf.Ticker(symbol)
    exps = ticker.options

    if len(exps) == 0:
        return
    
    df = pd.concat([ticker.option_chain(date=exps[0])[0], ticker.option_chain(date=exps[0])[0]])
    df["expiry"] = exps[0]
    for dt in exps[1:]:
        calls = ticker.option_chain(date=dt)[0]
        puts = ticker.option_chain(date=dt)[1]
        calls["expiry"] = dt
        puts["expiry"] = dt
        df = pd.concat([
            df, calls, puts
        ])
    return df


def get_name():
    dt = datetime.datetime.today()
    #return f"{dt.day}-{dt.month}-{dt.year} {dt.hour}:{dt.minute}"
    return f"{dt.year}-{dt.month}-{dt.day}"

name = get_name()

try:
    os.mkdir(name)
except Exception as err:
    print(err)

print(name)

for symb in all_symbols:
    try:
        print(symb, "...")
        data = get_symbol_data(symb)
        if len(data):
            data.to_csv(name + "/" + symb + ".csv")
            s3.upload_file(name + "/" + symb + ".csv", "791-options-data", name + "/" + symb + ".csv")
            print(len(data))

    except Exception as err:
        print(err)
 
os.system('sudo shutdown -h now')
