from yahoo_finance import Share
import csv
import pandas as pd

import pandas.io.data as web
import datetime

def download_stock(symbol):
    yahoo = Share(symbol)
    stocklist = yahoo.get_historical('2005-03-08', '2007-12-28')
    print len(stocklist)
    keys = stocklist[0].keys()
    with open('%s.csv' %symbol, 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(stocklist)

def read_stocks(symbollist):
    frames = [ read_stock(symbol) for symbol in symbollist ]
    result = pd.concat(frames,axis=1)
    result = result.fillna(method='ffill')
    print result
    return result

def read_stock(symbol):
    # for symbol in symbollist:
    ver=pd.read_csv("%s.csv" %symbol)
    frame = ver[['Date','Adj_Close']]
    frame = frame.set_index('Date')
    frame.rename(columns={'Adj_Close': symbol}, inplace=True)
    # print frame
    return frame

def clean_stock(symbollist):
    symbol = symbollist[0]
    ver=pd.read_csv("%s.csv" %symbol)

if __name__ == "__main__":
    symbollist = ['INF.L', 'PSON.L','REL.L','UBM.L'] #
    # for symbol in symbollist:
    #     download_stock(symbol)
    read_stocks(symbollist)