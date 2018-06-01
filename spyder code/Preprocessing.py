# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 09:27:23 2018

@author: Young Min Joung
"""

import pandas as pd
import numpy as np
           

#%% functions
def match_dateformat(df):
    

def find_holiday(file, year):
    holidays = ["New Year's Day", "Martin Luther King Jr. Day", "Valentine's Day",
       "President's Day", "Easter Sunday", "Mother's Day", "Memorial Day",
       "Father's Day", "Independence Day", "Labor Day", "Columbus Day",
       "Halloween", "Veterans Day", "Thanksgiving Day", "Black Friday",
       "Christmas Eve", "Christmas Day", "New Year's Eve"]
    
    holi = pd.read_excel(file, year, header=None)
    
    holiday = pd.DataFrame(columns=[0,1,2,3,4])

    for _ in holidays:
        for i in range(len(holi[2])):
            if _ == holi[2][i]:
                holiday = holiday.append(holi.loc[i])
    return holiday
b
def holiday_flag(holidayYr):
    dates = [date.split("-") for date in train['date']]
    years = [year for year in dates[0]]

#%%
holiday12 = find_holiday('data/holiday.xlsx', '2012')
holiday13 = find_holiday('data/holiday.xlsx', '2013')
holiday14 = find_holiday('data/holiday.xlsx', '2014')


train = pd.read_csv('data/train.csv')
weather = pd.read_csv('data/weather.csv')
key = pd.read_csv('data/key.csv')
test = pd.read_csv('data/test.csv')
sample = pd.read_csv('data/sampleSubmission.csv')



train = train.merge(key, left_on='store_nbr', right_on='store_nbr')
train_pivot = train.pivot_table(values='units', index=['date'], columns=['station_nbr','store_nbr','item_nbr'], aggfunc=np.sum)
#%%
weather = pd.read_csv('C:/Users/Young Min Joung/Documents/datascience/teamproject1/spyder code/data/weather.csv')

for i in range(len(weather['codesum'])):
    codesum = weather['codesum'][i].split(" ")
    for _ in codesum:
        if _ == 'RA':
            weather['rain_flag'] = 1
        elif _ == 'SN':
            weather['snow_flag'] = 1
        else: 
            weather['normal_flag'] = 1
            codesum = []
weather.head()




