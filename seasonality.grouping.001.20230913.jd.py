# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 10:53:17 2023

@author: johnd
"""

import pandas as pd
import datetime as dt
import numpy as np
import os
import time
import json
import calendar
import matplotlib.pyplot as plt
#%%
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 25)
#%%
config_path = "C:/Users/johnd/OneDrive/Desktop/"
file_name = 'rose.config.file.txt'
config_file = open(config_path+file_name, 'r')
config = json.load(config_file)
config_file.close()
rose_username = config['rose_username']
rose_password = config['rose_password']
#%%
from rose_wrapper.rose import Rose
rose = Rose()
rose.login(rose_username, rose_password)

#%%
"""
    Seaonality based on start of the year
"""
#examples code  - for signal - didn't work out
signal_rcode = 'fed.funds:change:min(0.2):sub(0.2):mult(1e20):max(1):since(2000)'
signal_df = rose.pull(signal_rcode)
#%%
#example code for testing - us equities
target_rcode = 'usa.eq:d' #use resample days - for consistency
target_df = rose.pull(target_rcode)

#break down date as target
target_df['year'] = target_df.index.year
target_df['month'] = target_df.index.month
target_df['day'] = target_df.index.day
target_df['month.day'] = target_df['month'].astype(str).str.zfill(2) + '-' + target_df['day'].astype(str).str.zfill(2)
#pivot based on month + day --> seasonality annual
pivot_df = target_df.pivot(index= 'month.day', columns = 'year', values = 'value')

pivot_normal_df = pivot_df.div(pivot_df.iloc[0])
pivot_normal_df = pivot_normal_df.multiply(100)
pivot_normal_df = pivot_normal_df.drop(['02-29'], axis = 0)

pivot_normal_df['since2000'] = pivot_normal_df[range(2000,2023)].mean(axis=1)
pivot_normal_df['all'] = pivot_normal_df.drop([2023], axis =1).mean(axis=1)

pivot_normal_df.plot(y=[2022, 2023, 'all', 'since2000'])

"""
    Seaonality based on start of the year - end
"""

#%%
""" Seasonality based on date map """

date_map = 'usa.yield.curve.inversion.dates.jd' #input

date_df = rose.pull(date_map)
#convert dates to datetime objects for manipulation

date_df['date.str'] = date_df['peak.inversion.dates'].astype(int).astype(str)
date_df['date'] = pd.to_datetime(date_df['date.str'], format = '%Y%m%d')

#find before and after dates - ~3months - 90d
days = 365 #input
date_df['early.date'] = date_df['date'] - pd.Timedelta(days, 'D')
date_df['late.date'] = date_df['date'] + pd.Timedelta(days, 'D')
#convert to string
date_df['early.date.str'] = date_df['early.date'].dt.strftime('%Y%m%d')
date_df['late.date.str'] = date_df['late.date'].dt.strftime('%Y%m%d')

duration = '10y'
c_title = f'usa.sov.bonds.{duration}.returns.excess'
stat_rcode_base = f'{c_title}.b.snow:return' #input
stat_rcode = stat_rcode_base + ':d'

transform = 'div'

if transform == 'sub':
    date_df['full_rosecode'] = stat_rcode + ':since(' + date_df['early.date.str'] +'):until(' + date_df['late.date.str'] + '):add(' + stat_rcode + ':mult(-1):until('  + date_df['date.str'] + '):last)'                     
elif transform == 'div':
    date_df['full_rosecode'] = stat_rcode + ':since(' + date_df['early.date.str'] +'):until(' + date_df['late.date.str'] + '):div(' + stat_rcode + ':until('  + date_df['date.str'] + '):last):mult(100)'
#%%
#pull rosecodes around those dates and align stats
temp_df_list = []
for rcode, date_str in zip(date_df['full_rosecode'], date_df['date.str']):
    #print(rcode)
    temp_df = rose.pull(rcode)
    #label based on central date
    temp_df.rename(columns = {'value':date_str}, inplace = True)
    temp_df.reset_index(inplace = True)
    #drop date axis for join
    temp_df.drop(['date'], axis = 1, inplace = True)
    temp_df_list.append(temp_df)
#%%
#joining all the data
final_df = pd.concat(temp_df_list, axis = 1)
final_df['mean'] = final_df.mean(axis=1)
#offsetting the data to midpoint
final_df['days'] = final_df.index - days
final_df = final_df.set_index('days')

# final_df.plot()
# plt.title('30y yield change')
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
#%%
stat_label = "" #"yield index" #input
x_axis_label = 'days from/to max inversion' #input
fig, ax = plt.subplots()
plt.title(f"{c_title} {stat_label}", fontsize = 24)
final_df.plot(figsize=(20,12), 
        lw=3, fontsize=16, ax=ax, grid=True)

for line in ax.get_lines():
    if line.get_label() == 'mean':
        line.set_linewidth(8)
        line.set_color('black')

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize = '16')
plt.xlabel(x_axis_label, fontsize = '20')
