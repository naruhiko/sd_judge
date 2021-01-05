#!/usr/bin/python
# -*- coding: utf-8 -*-

from statistics import stdev
from scipy import stats
import numpy as np
import pandas as pd

csvname = input('csvのファイルネームを入力: ')
data = pd.read_csv(csvname + '.csv')
print(data.head())

df1_name = input('対象の列の名前を入力(データ1):')
df2_name = input('対象の列の名前を入力(データ2):')
df1 = data.loc[:, df1_name]
df2 = data.loc[:, df2_name]

class Data:
    def __init__(self, name, data1, data2, user_p):
        self.name = name
        self.data1 = pd.read_csv(name + '.csv').loc[:, data1]
        self.data2 = pd.read_csv(name + '.csv').loc[:, data2]
        self.user_p = user_p
        self.datalist1 = list(self.data1.values.flatten())
        self.datalist2 = list(self.data2.values.flatten())

    @staticmethod
    def ask():
        return Data(
                input('filename?: '),
                input('data row name?: '),
                input('data2 row name?: '),
                input('pvalue?: ')
                )



class SdJudge(Data):
    def is_normal_dist(self, datalist1, user_p):
        result = stats.shapiro(datalist1)
        judge = bool(result[1] > user_p)
