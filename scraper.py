import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import os
import boto3
from symbols import all_symbols

BUCKET_NAME = "791-options-data"
s3 = boto3.client('s3')

def log(msg):
    current_dateTime = datetime.datetime.now()
    print(current_dateTime, msg)

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
    os.mkdir("/home/ec2-user/option_scraper/" + name)
    log("Created output directory")
except Exception as err:
    log("Error creating data directory")
    log(err)

print(name)

for symb in all_symbols[0:5]:
    try:
        log("Fetching symbol " + symb)
        data = get_symbol_data(symb)
        if data is not None and len(data):
            log("Fetched " + str(len(data)) + " lines")
            data.to_csv("/home/ec2-user/option_scraper/" + name + "/" + symb + ".csv")
            s3.upload_file("/home/ec2-user/option_scraper/" + name + "/" + symb + ".csv", "791-options-data", name + "/" + symb + ".csv")
            log("Pushed CSV to S3")

    except Exception as err:
        print("Error fetching data")
        print(err)

log("Script end")
