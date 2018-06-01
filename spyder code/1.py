# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 15:23:37 2018

@author: Young Min Joung
"""

import pandas as pd
import numpy as np

train = pd.read_csv('C:/Users/Young Min Joung/Documents/datascience/teamproject1/project1/data/train.csv')
weather = pd.read_csv('C:/Users/Young Min Joung/Documents/datascience/teamproject1/project1/data/weather.csv')
key = pd.read_csv('C:/Users/Young Min Joung/Documents/datascience/teamproject1/project1/data/key.csv')

def match_dateformat(df, year):
    """
    영문 월을 숫자 월로 바꾸어주고 나중에 사용하기 쉽도록 datetime.date 형태로 바꾸어주는 함수
    """
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for i in range(len(df)):
        dates = df.loc[i][0]
        dates = dates.split(" ")
        for j in range(len(months)):
            if dates[0] == months[j]:
                dates[0] = str(j + 1)
                dates_df = ["{} {} {}".format(year, dates[0], dates[1])]
                dates_df = pd.to_datetime(dates_df)
                df.loc[i][0] = dates_df.date[0]
    return df
def merge_holiday(holiday_df1, holiday_df2, holiday_df3):
    """
    각 연도별 공휴일 리스트 합치기
    """
    frame = [holiday_df1, holiday_df2, holiday_df3]
    holiday = pd.concat(frame).reset_index(drop=True)
    return holiday
def find_holiday(file, year):
    """
    수요에 영향을 미치는 주요 공휴일을 찾아내는 함수
    """
    holidays = ["New Year's Day", "Martin Luther King Jr. Day", "Valentine's Day",  "President's Day", "Easter Sunday", 
                      "Mother's Day", "Memorial Day", "Father's Day", "Independence Day", "Labor Day", "Columbus Day",
                      "Halloween", "Veterans Day", "Thanksgiving Day", "Black Friday", "Christmas Eve", "Christmas Day", "New Year's Eve"]
    
    holi = pd.read_excel(file, year, header=None)
    holi = match_dateformat(holi, year)
    holiday = pd.DataFrame(columns=[0,1,2,3,4])
    for _ in holidays:
        for i in range(len(holi[2])):
            if _ == holi[2][i]:
                holiday = holiday.append(holi.loc[i])
    return holiday
def TM_transform(series, T_replace, M_replace): 
    """
    데이터내의 T, M을 원하는 값으로 바꿔주는 함수
    """
    series = series.astype(str).map(lambda s: s.strip())
    series[series == 'T'] = T_replace
    series[series =='M'] = M_replace
    return series.astype('float')

def preprocessing(df, holiday):
    """
    train데이터를 가공하는 함수
    """
    df['units'] = np.log(df['units'] + 1)
    df['date'] = pd.to_datetime(df['date'])
    df['weekday'] = df.date.dt.weekday  # 월요일이 0 일요일이 6
    df['weekend'] = df.date.dt.weekday.isin([5, 6])  # 5: 토요일, 6: 일요일

    df['holiday'] = df.date.isin(holiday[0])
    df['weekday_holiday'] = df.holiday & (df.weekend == False)
    df['weekend_holiday'] = df.holiday & df.weekend

    # There are values that are computed as being "normal" for a given location. Normal are computed based on 30 years worth of data every ten years. (today temp - normal) = depart
    weather['data'] = pd.to_datetime(weather['date']) #weather는 글로벌변수
    for i in range(len(weather['codesum'])):
        codesum = weather['codesum'][i].split(" ")
        for _ in codesum:
            if _ == 'RA':
                weather.set_value(i, 'rain_flag', 1)
            elif _ == 'SN':
                weather.set_value(i, 'snow_flag', 1)
            elif _ == "":
                weather.set_value(i, 'normal_flag', 1)
            else:
                weather.set_value(i, 'abnormal_flag', 1)

    # return x or y depending on the condition
    weather['preciptotal'] = TM_transform(weather['preciptotal'], 0.005, 0.00)
    weather['preciptotal_flag'] = np.where(weather['preciptotal'] > 0.2, 1, 0)
    weather['depart'] = TM_transform(weather['depart'], np.nan, 0.00)
    weather['depart_flag'] = np.where(weather['depart'] > 8.0, 1, 0)
    weather['depart_flag'] = np.where(weather['depart'] < 8.0, -1, 0)
    
    return df

holiday12 = find_holiday('C:/Users/Young Min Joung/Documents/datascience/teamproject1/project1/data/holiday.xlsx', '2012')
holiday13 = find_holiday('C:/Users/Young Min Joung/Documents/datascience/teamproject1/project1/data/holiday.xlsx', '2013')
holiday14 = find_holiday('C:/Users/Young Min Joung/Documents/datascience/teamproject1/project1/data/holiday.xlsx', '2014')
holiday = merge_holiday(holiday12, holiday13, holiday14)
processed_train = preprocessing(train, holiday)