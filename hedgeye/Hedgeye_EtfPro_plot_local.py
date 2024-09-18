# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 11:55:52 2020

@author: JDSeelig
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 15:22:20 2020

@author: JDSeelig
"""
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import openpyxl
from openpyxl import Workbook
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

#from os import listdir
#from os.path import isfile, join
#onlyfiles = [f for f in listdir(path1) if isfile(join(path1, f))]
#%%
path1 = 'C:/Users/JDSeelig/Desktop/21_Statelligence/Hedgeye/'
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(path1) if isfile(join(path1, f))]
#print(onlyfiles)
#%%
#import xlrd 
  
loc = (path1 + 'Hedgeye_EPL.xlsx') 
  
#wb = xlrd.open_workbook(loc) 
#sheet = wb.sheet_by_index(0) 
  
# For row 0 and column 0 
#print(sheet.cell_value(0, 0) )
  
# Extracting number of columns 
#print(sheet.ncols)

#%%
k = []
for i in pd.read_excel(loc, sheet_name = None):
    dftemp = pd.read_excel(loc, sheet_name=i)
    dftemp['DATE'] = i
    k.append(dftemp)
#%%
df_final = pd.concat(k)
#df_final.dropna(inplace = True)

#%%
scol = 'DIRECTION'
sigcond = [df_final[scol] == 'BEARISH', df_final[scol] == 'NEUTRAL', df_final[scol] == 'BULLISH']
sigres = [-1,0,1]
df_final['BISIG'] = np.select(sigcond, sigres, default = 0)
df_final['DATE2'] = pd.to_datetime(df_final['DATE'], format = '%Y-%m-%d')

#%%

def hedgeyeplot (dft):
    plt.figure(figsize = (10,10))
    plt.subplot(211)
    plt.title(i, fontsize = 12, weight = 'bold')
    plt.xticks(fontsize = 10, weight = 'bold')
    plt.yticks(fontsize = 10,  weight = 'bold')
    plt.plot(dft['DATE2'], dft['BUY TRADE'],'g')
    plt.plot(dft['DATE2'], dft['SELL TRADE'],'r')
    plt.plot(dft['DATE2'], dft['CLOSE'])
    plt.plot(dft['DATE2'], dft['PREV. CLOSE'], 'bo')
    plt.ylabel('Price', fontsize = 12,  weight = 'bold')
    plt.subplot(212)
    plt.xticks(fontsize = 10, weight = 'bold')
    plt.yticks(fontsize = 10,  weight = 'bold')
    plt.plot(dft['DATE2'], dft['BISIG'])
    plt.ylim([-1.05,1.05])
    plt.xlabel('Date', fontsize = 12,  weight = 'bold')
    plt.show()
#%%
l = []
m = []
pos_list = []
for i in list(df_final.TICKER.unique()):
    
    dff = df_final[df_final.TICKER == i].copy()
    dff.sort_values(by = 'DATE2', inplace = True)
    dff.reset_index(inplace = True)
    dff.drop('index', axis = 1, inplace = True)
    dff['DELTA_DAYS'] = dff.DATE2.diff().dt.days
    dff['BOX_X'] = np.where(dff['DELTA_DAYS']>10,1,0)
    dff['BOX'] = dff['BOX_X'].cumsum()
    #hedgeyeplot(dff)
    dff.fillna(0,inplace  = True)
    for j in dff.BOX.unique():   
        posy = []
        posy.append(i)         
        dfft = dff[dff.BOX == j].copy()
        dfft.reset_index(inplace = True)
        dfft.drop('index',axis = 1, inplace = True)
        if len(dfft) > 2:
            #print(j, '\t',len(dfft))
            #print(dfft)
            if dfft['CO PRICE'].iloc[0] == 0:
                beginp = dfft['RECENT PRICE'].iloc[0]
                begindays = dfft['DATE2'].iloc[0]
            else:
                beginp = dfft['CO PRICE'].iloc[0]
                begindays = dfft['CO'].iloc[0]
            if dfft['CO PRICE'].iloc[-1] == 0:
                endp = dfft['RECENT PRICE'].iloc[-1]
                enddays = dfft['DATE2'].iloc[-1]
            else:
                endp = dfft['CO PRICE'].iloc[-1]
                enddays = dfft['CO'].iloc[-1]
            sig = dfft.BISIG.iloc[0]
            #print (i, beginp, endp, sig)
            if (sig == 1):
                val = (endp - beginp)/beginp
            else:
                val = 0.5*(beginp - endp)/beginp
            
            ddays = (enddays - begindays).days
            posy.append(sig)
            posy.append(begindays)
            posy.append(enddays)
            posy.append(beginp)
            posy.append(endp)
            l.append(val)
            m.append(ddays)
            #print(len(posy))
            pos_list.append(posy)
            
    #dff['CLOSE'] = dff['PREV. CLOSE'].shift(-1)
    #hedgeyeplot(dff)
#%%
posydf = pd.DataFrame(pos_list, columns = ['ticker', 'signal','date.start', 'date.end', 'price.start', 'price.end'])
loc_out = (path1 + 'Hedgeye_EPL_out.xlsx')
posydf.to_excel(loc_out)
#%%
n_list = []
p_list = []
for k in l:
    if k>=0:
        p_list.append(k)
    else:
        n_list.append(k)
#neg_count = len(list(filter(lambda x: (x <0), l)))
#pos_count = len(list(filter(lambda x: (x >=0), l)))
winpct = round(len(p_list)/len(l),3)
l_avg = round(sum(l)/len(l),3)
n_avg = round(sum(n_list)/len(n_list),3)
p_avg = round(sum(p_list)/len(p_list),3)
print('\n\nHedgeye ETF Pro Results\n',
      'return: ',round(sum(l),3), '\tavgholdtime: ',round(sum(m)/len(m),0),'\t# Ideas:', len(l),
      '\nwinpct: ', winpct, '\tavg: ', 
      l_avg, '\npos avg: ', p_avg,'\tneg avg: ',n_avg)
    
