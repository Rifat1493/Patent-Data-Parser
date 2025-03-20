# -*- coding: utf-8 -*-
"""
Created on Thu May  2 21:47:04 2024

@author: Rifat1493
"""

import os
import pandas as pd

path = 'Data/'

filenames = os.listdir(path)

df = pd.read_excel(path+filenames[0], sheet_name="Sheet1")

filenames.pop(0)

for i in filenames:
    
    print(i)
    df1 = pd.read_excel(path+i, sheet_name="Sheet1")
    
    df=pd.merge(df, df1, on='Company Name', how='outer')
    


df.to_excel('merged.xlsx', sheet_name='sheet1', index=False)



import pandas as pd



df = pd.read_excel("rr_merged.xlsx")
df = df.drop(['Percent Change', '% Change_x', '% change', '% Change_y','% Change'], axis=1)

df_nonempty = df.fillna(0)

df_grouped = df_nonempty.groupby("Company Name").sum()


df_nonempty.dtypes

df_grouped.to_excel('curated_data.xlsx', sheet_name='sheet1', index=True)








# Find ticker industry name sector name

import requests
from tqdm import tqdm

def get_ticker (company_name):
    url = "https://query2.finance.yahoo.com/v1/finance/search"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    params = {"q": company_name, "quotes_count": 1, "country": "United States"}

    res = requests.get(url=url, params=params, headers={'User-Agent': user_agent})
    data = res.json()
    print(data)
    ticker = data['quotes'][0]['symbol']
    industry = data['quotes'][0]['industry']
    sector = data['quotes'][0]['sector']
    return ticker, industry, sector


import pandas as pd

df = pd.read_excel("Transformed Data/raw data.xlsx")

#df =df.head(20)

#company_names_lst = df["Company Name"].tolist()
company_names_lst= ['Daicel Chemical Industries Ltd.']
ticker_lst =[]
industry_lst =[]
sector_lst = []


for company_name in tqdm( company_names_lst):
    try:
        ticker, industry, sector = get_ticker(company_name)
        ticker_lst.append(ticker)
        industry_lst.append(industry)
        sector_lst.append(sector)
    except Exception as e:
        ticker_lst.append(None)
        industry_lst.append(None)
        sector_lst.append(None)



df ["Ticker"] = ticker_lst

df ["Industry"] = industry_lst

df ["Sector"] = sector_lst


df.to_excel('curated_data_with_tickers.xlsx', sheet_name='sheet1', index=True)
    