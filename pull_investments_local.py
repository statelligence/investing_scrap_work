# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 10:47:05 2020

@author: JDSeelig
"""
import pandas as pd
import datetime as dt
import numpy as np
from os import listdir
from os.path import isfile, join
#%%
basepath = "C:/Users/JDSeelig/Desktop/21_Statelligence/Invest_Book/"
date = '2020-12-26'
path = basepath + '/Invest_Drop/' +date
#%%
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
print (onlyfiles)
#%%
def schwabread(specPath, fileName):
    df = pd.read_csv(specPath+'/'+ fileName)
    k = df.columns[0]
    j = str(k).split()
    l = ' '.join(j[3:6])
    df = pd.read_csv(specPath+'/'+ fileName,skiprows = 2)
    df.fillna(0, inplace = True)
    #ctk - columns to keep
    ctk = ['Symbol', 'Quantity', 'Price', 'Market Value', 'Cost Basis', 'Dividend Yield', 'Description','Ex-Dividend Date']
    dfmod = df[ctk].copy()
    dfmod[['TICKER','EYDATE','STRIKE','TYPE']] = dfmod['Symbol'].str.split(expand = True)
    dfmod['EYDATE'].replace({'&':np.nan}, inplace = True)
    dfmod['STRIKE'].replace({np.nan:0, 'Cash':0}, inplace = True)
    dfmod['TYPE'].replace({np.nan:'E', 'Investments':'E'},inplace = True)
    dfmod = dfmod[dfmod['Symbol'] != 'Account Total']
    dfmod.columns = dfmod.columns.str.replace(' ', '')
    #these will be ubiquitious names/ columns if possible
    dfmod.rename(columns={'Description':'NAME', 'Quantity':'QTY', 'Price':'PRICE','MarketValue':'VALUE', 
                          'CostBasis':'COST', 'DividendYield':'YIELD', 'Ex-DividendDate':'EXDATE'}, inplace = True)
    dfmod.drop('Symbol',axis = 1,inplace = True)
    dfmod['ACT'] = l
    dfmod['LOC'] = 'Schwab'
    return dfmod
#%%
def fidelread(specPath, fileName):
    df = pd.read_csv(specPath + '/' + fileName)
    marker = df.iloc[0,0]
    dfmod = df[df['Account Name/Number'] == marker].copy()
    ctk = ['Symbol', 'Description', 'Quantity', 'Last Price', 'Current Value', 'Cost Basis Total', 'Account Name/Number']
    dfmod2 = dfmod[ctk].copy()
    dfmod2['Symbol'].replace({'CORE**':'Cash'}, inplace = True)
    dfmod2.rename(columns = {'Symbol': 'TICKER', 'Description':'NAME', 'Quantity':'QTY', 'Last Price': 'PRICE',
                            'Current Value':'VALUE', 'Cost Basis Total': 'COST', 'Account Name/Number':'ACT'}, inplace = True)
    dfmod2['LOC'] = 'Fidelity'
    return dfmod2
#%%
dftry = pd.read_csv(path+'/'+ onlyfiles[0])