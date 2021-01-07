#!/usr/bin/python
# -*- coding: utf-8 -*-

from statistics import stdev
from scipy import stats
import numpy as np
import pandas as pd
import decimal


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
        else:
            pvalue = float(pvalue)

        filename = input('filename?: ')
        print(pd.read_csv(filename + '.csv').head())

        while True:
            is_rel = input('is it relative?[[y]/n]: ')
            if is_rel == 'y' or is_rel == 'n' or is_rel == '':
                break
            else:
                print('enter correctly, once more.')
        return SdJudge(
                filename,
                input('data row name?: '),
                input('data2 row name?: ') or 'none',
                pvalue,
                is_rel
                ), is_rel



    def is_normal_dist(self):
        result_1 = stats.shapiro(self.datalist1)
        judge_1 = bool(result_1[1] > self.user_p)
        result_2 = stats.shapiro(self.datalist2)
        judge_2 = bool(result_2[1] > self.user_p)
        judge = bool(judge_1 and judge_2) # if judge_1 and judge_2 is true, judge is true. otherwise False.
        return judge_1, judge_2, judge, result_1[1], result_2[1]


    def variance_bartlett(self):
        result = stats.bartlett(self.datalist1, self.datalist2)
        judge = bool(result[1] > self.user_p)
        return judge, result[1]


    def variance_levene(self):
        result = stats.levene(self.datalist1, self.datalist2)
        judge = bool(result[1] > self.user_p)
        return judge, result[1]


    def ttest_student_rel(self):
        result = stats.ttest_rel(self.datalist1, self.datalist2)
        judge = bool(result[1] > self.user_p)
        return judge, result[1]


    def ttest_student_ind(self):
        result = stats.ttest_ind(self.datalist1, self.datalist2)
        judge = bool(result[1] > self.user_p)
        return judge, result[1]


    def ttest_welch(self):
        result = stats.ttest_ind(self.datalist1, self.datalist2, equal_var=False)
        judge = bool(result[1] > self.user_p) 
        return judge, result[1]


    def mann(self):
        result = stats.mannwhitneyu(self.datalist1, self.datalist2, alternative='two-sided')
        judge = bool(result[1] > self.user_p)
        return judge, result[1]


    def wilcoxon_signed(self):
        result = stats.wilcoxon(self.datalist1, self.datalist2, correction=True)
        judge = bool(result[1] > self.user_p)
        return judge, result[1]


if __name__ == '__main__':
    usr = SdJudge.ask()
    norm_result = SdJudge.is_normal_dist(usr[0])
    print('data1 is normal distribution: {}, p={} \ndata2 is normal distribution: {}, p={}'.format(norm_result[0], norm_result[3], norm_result[1], norm_result[4]))
    if norm_result[2] is True:
        bart_result = SdJudge.variance_bartlett(usr[0])
        print('Bartlett normal dist. kai2zero : {}, p={}'.format(bart_result[0], bart_result[1]))
        if  usr[1]== 'y' or usr[1] == '':
            if bart_result[0] is True:
                t_ind_result = SdJudge.ttest_student_ind(usr[0])
                print('t test indivisual student : {}, p={}'.format(t_ind_result[0], t_ind_result[1]))
            else:
                t_welch_result = SdJudge.ttest_welch(usr[0])
                print('t test indivisual welch : {}, p={}'.format(t_welch_result[0], t_welch_result[1]))
        elif usr[1] == 'n':
            t_rel_result = SdJudge.ttest_student_rel(usr[0])
            print('t test relative : {}, p={}'.format(t_rel_result[0], t_rel_result[1]))
    else:
        levene_result = SdJudge.variance_levene(usr[0])
        print('Levene not normal dist. : {}, p={}'.format(levene_result[0], levene_result[1]))
        if usr[1]== 'y' or usr[1] == '':
            mann_result = SdJudge.mann(usr[0])
            print('Mann-whitney not normal dist. : {}, p={}'.format(mann_result[0], mann_result[1]))
        elif usr[1]== 'n':
            wilc_result = SdJudge.wilcoxon_signed(usr[0])
            print('Wilcoxon Signed-rank : {}, p={}'.format(wilc_result[0], wilc_result[1]))
