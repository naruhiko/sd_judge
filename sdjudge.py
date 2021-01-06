#!/usr/bin/python
# -*- coding: utf-8 -*-

from statistics import stdev
from scipy import stats
import numpy as np
import pandas as pd


class SdJudge:
    def __init__(self, name, data1, data2, user_p, is_rel):
        self.name = name
        self.data1 = pd.read_csv(name + '.csv').loc[:, data1]
        self.data2 = pd.read_csv(name + '.csv').loc[:, data2]
        self.user_p = user_p
        self.datalist1 = list(self.data1.values.flatten())
        self.datalist2 = list(self.data2.values.flatten())

    @staticmethod
    def ask():
        pvalue = input('pvalue?: ')
        if len(pvalue) == 0:
            pvalue = 0.05
        while True:
            is_rel = input('is it relative?[y/n]: ')
            if is_rel == 'y' or is_rel == 'n':
                break
            else:
                print('enter correctly, once more.')
        return SdJudge(
                input('filename?: '),
                input('data row name?: '),
                input('data2 row name?: ') or 'none',
                pvalue,
                is_rel
                )



    def is_normal_dist(self, datalist1, datalist2, user_p):
        result_1 = stats.shapiro(datalist1)
        judge_1 = bool(result_1[1] > user_p)
        result_2 = stats.shapiro(datalist2)
        judge_2 = bool(result_2[1] > user_p)
        judge = bool(judge_1 and judge_2) # if judge_1 and judge_2 is true, judge is true. otherwise False.
        return judge_1, judge_2, judge


    def variance_bartlett(self, datalist1, datalist2, user_p):
        result = stats.bartlett(datalist1, datalist2)
        judge = bool(result[1] > user_p)
        return judge, result[1]


    def variance_levene(self, datalist1, datalist2, user_p):
        result = stats.levene(datalist1, datalist2)
        judge = bool(result[1] > user_p)
        return judge, result[1]


    def ttest_student_rel(self, datalist1, datalist2, user_p):
        result = stats.ttest_rel(datalist1, datalist2)
        judge = bool(result[1] > user_p)
        return judge, result[1]


    def ttest_student_ind(self, datalist1, datalist2, user_p):
        result = stats.ttest_ind(datalist1, datalist2)
        judge = bool(result[1] > user_p)
        return judge, result[1]


    def ttest_welch(self, datalist1, datalist2, user_p):
        result = stats.ttest_ind(datalist1, datalist2, equal_var=False)
        judge = bool(result[1] > user_p)
        return judge, result[1]


    def mann(self, datalist1, datalist2, user_p):
        result = stats.mannwhitneyu(datalist1, datalist2, alternative='two-sided')
        judge = bool(result[1] > user_p)
        return judge, result[1]


    def wilcoxon_signed(self, datalist1, datalist2, user_p):
        result = stats.wilcoxon(datalist1, datalist2, correction=True)
        judge = bool(result[1] > user_p)
        return judge, result[1]
