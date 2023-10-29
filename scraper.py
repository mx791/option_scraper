import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import os

csv_symbs = pd.read_csv("./symbols.csv")["Symbol"].values
all_symbols = [
    '^VIX',
    '^SPX',
    *csv_symbs
]


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
    return f"{dt.day}-{dt.month}-{dt.year} {dt.hour}:{dt.minute}"

name = get_name()

try:
    os.mkdir(name)
except:
    pass

for symb in all_symbols:
    try:
        data = get_symbol_data(symb)
        if len(data):
            data.to_csv(name + "/" + symb + ".csv")
            print(symb, len(data))

    except Exception as err:
        pass