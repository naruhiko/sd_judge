#!/usr/bin/python
# -*- coding: utf-8 -*-

from statistics import stdev
from scipy import stats
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')

csvname = input('csvのファイルネームを入力: ')
data = pd.read_csv(csvname + '.csv')
print(data.head())
#df_beer = data.iloc[:, [1]]
#df_b_beer = data.iloc[:, [2]]

df1_name = input('対象の列の名前を入力(データ1):')
df2_name = input('対象の列の名前を入力(データ2):')
df1 = data.loc[:, df1_name]
df2 = data.loc[:, df2_name]

class Data:
    def __init__(self, name, data1, data2):
        self.name = name
        self.data1 = data1
        self.data2 = data2

    def listize(self):
        df1 = list(self.data1.values.flatten())
        df2 = list(self.data2.values.flatten())
