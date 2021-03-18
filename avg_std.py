import pandas as pd
import numpy as np
import json
import requests
import datetime


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

    history_average = []
    
    code = str(input("code number: "))
    for last_year in range(2):
        current_year = year - last_year
        year_average = []
        for first in [6,0]:
            season_average = []
            
            for m in range(first+6, first, -1):
                if last_year == 0 and m > month:
                    continue

                m_ = '0' + str(m) if m < 10 else str(m)

                data = Get_StockPrice(code ,f'{current_year}{m_}01' )
                month_average = np.average(data['Close'])

                if current_year == year and m == month:
                    month_std = np.std(data['Close'])
                    print(f'{current_year}/{m} month average : {month_average}')
                    print(f'{current_year}/{m} month std : {month_std}')
                    print(f'{current_year}/{m} suggestion month price : {month_average - month_std} ~ {month_average - 2*month_std}')
                    
                season_average.append(month_average)
                year_average.append(month_average)
                history_average.append(month_average)

            if not season_average or last_year != 0:
                continue

            season_std = np.std(season_average)
            season_average = np.average(season_average)
            
            print(f'{current_year}/{first} season average : {season_average}')
            print(f'{current_year}/{first} season std : {season_std}')
            print(f'{current_year}/{first} suggestion season price : {season_average - season_std} ~ {season_average - 2*season_std}')
        
        if last_year == 0:

            year_std = np.std(year_average)
            year_average = np.average(year_average)

            print(f'{current_year} year average : {year_average}')
            print(f'{current_year} year std : {year_std}')
            print(f'{current_year} suggestion year price : {year_average - year_std} ~ {year_average - 2*year_std}')
            
    history_std = np.std(history_average)
    history_average = np.average(history_average)

    print(f'history average : {history_average}')
    print(f'history std : {history_std}')
    print(f'history price : {history_average - history_std} ~ {history_average - 2*history_std}')


            


