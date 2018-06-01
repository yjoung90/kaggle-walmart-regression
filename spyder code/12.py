# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 13:37:42 2018

@author: Young Min Joung
"""
import pandas as pd
import numpy as np


train = pd.read_csv('C:/Users/Young Min Joung/Documents/datascience/teamproject1/project1/data/train.csv')
weather = pd.read_csv('C:/Users/Young Min Joung/Documents/datascience/teamproject1/project1/data/weather.csv')
key = pd.read_csv('C:/Users/Young Min Joung/Documents/datascience/teamproject1/project1/data/key.csv')

train = pd.merge(train, key, on='store_nbr')