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
#from os.path import isfile, join}
#onlyfiles = [f for f in listdir(path1) if isfile(join(path1, f))]
#%%
path1 = 'C:/Users/JDSeelig/Desktop/21_Statelligence/Hedgeye/'
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(path1) if isfile(join(path1, f))]
#print(onlyfiles)
#%%
#import xlrd 
  
loc = (path1 + 'Hedgeye_RR.xlsx') 
  
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
df_final.dropna(inplace = True)
#%%
newids = df_final['INDEX'].str.split(" ", n = 1, expand = True)
df_final['TICKER'] = newids[0]
df_final['SIGNAL'] = newids[1]
df_final.drop(columns = ['INDEX'], inplace = True)
#%%
scol = 'SIGNAL'
sigcond = [df_final[scol] == '(BEARISH)', df_final[scol] == '(NEUTRAL)', df_final[scol] == '(BULLISH)']
sigres = [-1,0,1]
df_final['BISIG'] = np.select(sigcond, sigres, default = 0)


#%%
df_final['DATE2'] = pd.to_datetime(df_final['DATE'], format = '%Y-%m-%d')
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
for i in df_final.TICKER.unique():
    print(len(i))
    dff = df_final[df_final.TICKER == i]
    dff['CLOSE'] = dff['PREV. CLOSE'].shift(-1)
    hedgeyeplot(dff)
    