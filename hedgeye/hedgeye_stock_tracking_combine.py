# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 09:18:00 2020

@author: JDSeelig
"""

import pandas as pd
import datetime as dt
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
#import openpyxl
#from openpyxl import Workbook
import re
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
#%%
path1 = 'C:/Users/JDSeelig/Desktop/21_Statelligence/Hedgeye/'
date = '2020-10-05'
#%%
def indexsig (df_enter, title):
    if 'INDEX' in df_enter.columns: 
        newids = df_enter['INDEX'].str.split(" ", n = 1, expand = True)
        df_enter['TICKER'] = newids[0]
        df_enter['SIGNAL'] = newids[1]
        df_enter.drop(columns = ['INDEX'], inplace = True)
    if 'DIRECTION' in df_enter.columns:
        df_enter.rename({'DIRECTION':'SIGNAL'}, axis = 1, inplace = True)
    low_keys = ['L TREND RANGE', 'L TREND', 'BUY TRADE']
    for lk in low_keys:
        if lk in df_enter.columns:
            df_enter.rename({lk:'LTR'}, axis = 1, inplace = True)
    high_keys = ['H TREND RANGE', 'H TREND', 'SELL TRADE']
    for hk in high_keys:
        if hk in df_enter.columns:
            df_enter.rename({hk:'HTR'}, axis = 1, inplace = True)
    price_keys = ['RECENT PRICE', 'PREV. CLOSE', 'CLOSING PRICE']
    for pk in price_keys:
        if pk in df_enter.columns:
            df_enter.rename({pk: 'PRICE'}, axis = 1, inplace = True)
    df_enter['SIGNAL'] = df_enter['SIGNAL'].map(lambda x: x.lstrip('(').rstrip(')').strip())
    
    #print(df_enter)
    scol = 'SIGNAL'
    sigcond = [df_enter[scol] == 'BEARISH', df_enter[scol] == 'NEUTRAL', df_enter[scol] == 'BULLISH']
    sigres = [-1,0,1]
    df_enter['BISIG'] = np.select(sigcond, sigres, default = 0)
    if 'CO' in df_enter.columns:
        df_enter['TD'] = np.where( df_enter.CO.notnull() & df_enter.LTR.notnull(), 1, 0)
        df_enter['PRICE'] = np.where(df_enter['CO PRICE'].notnull(), df_enter['CO PRICE'], df_enter['PRICE'])
        df_exit = df_enter[df_enter.TD== 0].copy()
    else:
        df_exit = df_enter.copy()
    df_exit['FILE'] = title
    df_exit = df_exit[['TICKER', 'PRICE', 'HTR', 'LTR', 'BISIG', 'FILE']]
    #print(df_exit)
    return (df_exit)
#%%
fnames = ['Hedgeye_EPL.xlsx', 'Hedgeye_RR.xlsx', 'Hedgeye_II.xlsx']
df_list = []
for fname in fnames:
    print(fname)
    j = re.split('[._]',fname)
    loc = path1 + fname
    xl = pd.ExcelFile(loc)
    snames = np.array(xl.sheet_names, dtype = 'datetime64')
    key_sname = np.amax(snames)
    #print(key_sname)
    df = pd.read_excel(loc, sheet_name = np.datetime_as_string(key_sname) )
    df_return = indexsig(df, j[1])
    #print (df_return.keys())
    df_list.append(df_return)

#%%

#sndates = dt.datetime.strptime([snames], '"%Y-%m-%d"').date()
#for i in pd.read_excel(loc, sheet_name = None):
#    print(i)
#    dftemp = pd.read_excel(loc, sheet_name=i)
#    dftemp['DATE'] = i
#    k.append(dftemp)
#%%
df_final = pd.concat(df_list)
df_final.sort_values(['TICKER'], axis = 0, inplace = True)
df_final.reset_index(inplace = True)
df_final.drop('index', axis = 1, inplace = True)
df_final['ptsAvl'] = np.where(df_final['BISIG']==1,df_final['HTR']-df_final['PRICE'], df_final['PRICE']-df_final['LTR'])
df_final['pctAvl'] = round(df_final['ptsAvl']/(df_final['HTR']-df_final['LTR']),4)
df_final.to_csv(path1+'Combo_Tracker/'+'HC_'+date+'.csv')