import pandas as pd
import numpy as np
import json
import requests
import datetime

def Get_100rank():
    rk = pd.read_csv('StockList.csv')
    rk['代號'] = rk['代號'].str.replace('=','')
    rk['代號'] = rk['代號'].str.replace('"','').astype(int)
    return rk['代號'][0:100]

def Get_StockPrice(Symbol, Date):

    url = f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={Date}&stockNo={Symbol}'
    
    data = requests.get(url).text
    json_data = json.loads(data)
    
    Stock_data = json_data['data']
    
    StockPrice = pd.DataFrame(Stock_data, columns = ['Date','Volume','Volume_Cash','Open','High','Low','Close','Change','Order'])
    
    StockPrice['Date'] = StockPrice['Date'].str.replace('/','').astype(int) + 19110000
    StockPrice['Date'] = pd.to_datetime(StockPrice['Date'].astype(str))
    StockPrice['Volume'] = StockPrice['Volume'].str.replace(',','').astype(float)/1000
    StockPrice['Volume_Cash'] = StockPrice['Volume_Cash'].str.replace(',','').astype(float)
    StockPrice['Order'] = StockPrice['Order'].str.replace(',','').astype(float)
    
    StockPrice['Open'] = StockPrice['Open'].str.replace(',','').astype(float)
    StockPrice['High'] = StockPrice['High'].str.replace(',','').astype(float)
    StockPrice['Low'] = StockPrice['Low'].str.replace(',','').astype(float)
    StockPrice['Close'] = StockPrice['Close'].str.replace(',','').astype(float)

    StockPrice = StockPrice.set_index('Date', drop = True)


    StockPrice = StockPrice[['Open','High','Low','Close','Volume']]
    return StockPrice

if __name__ == '__main__':
    year = datetime.date.today().year
    month = datetime.date.today().month

    rk = Get_100rank()
    for name_code in rk:
        for last_year in range(0,3):
            for m in range(1,13):
                if last_year == 0 and m > month:
                    continue

                m = '0' + str(m) if m < 10 else str(m)

                data = Get_StockPrice(name_code, str(year-last_year) + m + '01' )
                print(data)
                
            break
        break