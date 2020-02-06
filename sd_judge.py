
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
import inspect
import matplotlib.pyplot as plt
from statistics import stdev
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
# print(df_beer)
# df_b_beer.head()
user_p = input('p値を変更する場合は入力(Enterでデフォルトp=0.05): ')
if len(user_p) == 0:
        user_p = 0.05


def listize(dataframe):
        listize_item = list(dataframe.values.flatten())
        return listize_item


def is_norm_dist(df):
        li = listize(df)
        result = stats.shapiro(li)
        statistics = result[0]
        pvalue = result[1]

        if pvalue > user_p:
                judge = '正規分布に従う'
        else:
                judge = '正規分布に従わない'

        # print('W=', result[0], ' p=', result[1], ' ', judge, sep='')
        return statistics, pvalue, judge


def variance_bartlett(df1, df2):
        li1 = listize(df1)
        li2 = listize(df2)
        result = stats.bartlett(li1, li2)
        statistics = result[0]
        pvalue = result[1]

        if pvalue > user_p:
                judge = '等分散である'
        else:
                judge = '等分散でない'

        return statistics, pvalue, judge


def variance_levene(df1, df2):
        li1 = listize(df1)
        li2 = listize(df2)
        result = stats.levene(li1, li2)
        statistics = result[0]
        pvalue = result[1]

        if pvalue > user_p:
                judge = '等分散である'
        else:
                judge = '等分散でない'

        return statistics, pvalue, judge


def ttest_student_rel(df1 , df2):
        li1 = listize(df1)
        li2 = listize(df2)
        result = stats.ttest_rel(li1, li2)
        statistics = result[0]
        pvalue = result[1]

        if pvalue > user_p:
                judge = '有意差はない'
        else:
                judge = '有意差がある'

        return statistics, pvalue, judge


def ttest_student_ind(df1 , df2):
        li1 = listize(df1)
        li2 = listize(df2)
        result = stats.ttest_ind(li1, li2)
        statistics = result[0]
        pvalue = result[1]

        if pvalue > user_p:
                judge = '有意差はない'
        else:
                judge = '有意差がある'

        return statistics, pvalue, judge


def ttest_welch(df1 , df2):
        li1 = listize(df1)
        li2 = listize(df2)
        result = stats.ttest_ind(li1, li2, equal_var=False)
        statistics = result[0]
        pvalue = result[1]

        if pvalue > user_p:
                judge = '有意差はない'
        else:
                judge = '有意差がある'

        return statistics, pvalue, judge


def mann(df1 , df2):
        li1 = listize(df1)
        li2 = listize(df2)
        result = stats.mannwhitneyu(li1, li2, alternative='two-sided')
        statistics = result[0]
        pvalue = result[1]

        if pvalue > user_p:
                judge = '有意差はない'
        else:
                judge = '有意差がある'

        return statistics, pvalue, judge


def wilcoxon_signed(df1 , df2):
        li1 = listize(df1)
        li2 = listize(df2)
        result = stats.wilcoxon(li1, li2, correction=True)
        statistics = result[0]
        pvalue = result[1]

        if pvalue > user_p:
                judge = '有意差はない'
        else:
                judge = '有意差がある'

        return statistics, pvalue, judge


while True:
        is_rel = input('2群は独立であるか？ y/n: ')
        if is_rel == 'y' or is_rel == 'n':
                break
        else:
                print('ちゃんと半角で入力して！！！\n')


df1_norm_result = is_norm_dist(df1)
print('\n', df1_name, ': W=', df1_norm_result[0], ', p=', df1_norm_result[1], ',  jud: ', df1_norm_result[2], sep='')

df2_norm_result = is_norm_dist(df2)
print(df2_name, ': W=', df2_norm_result[0], ', p=', df2_norm_result[1], ',  jud: ', df2_norm_result[2], sep='')


if is_norm_dist(df1)[1] > user_p and is_norm_dist(df2)[1] > user_p:
        bart_result = variance_bartlett(df1, df2)
        print('Bartlett検定(正規分布を仮定): kai2zero=', bart_result[0], ', p=', bart_result[1], ',  jud: ', bart_result[2], sep='')
        variance = bart_result[1]

        if is_rel == 'y':
                if variance > user_p:
                        t_stu_ind_result = ttest_student_ind(df1, df2)
                        print('独立2群のt検定(等分散・正規分布を仮定):　t=', t_stu_ind_result[0], ', p=', t_stu_ind_result[1], ',  jud: ',
                        t_stu_ind_result[2], sep='')
                else:
                        t_welch = ttest_welch(df1, df2)
                        print('独立2群のt検定(非等分散・正規分布を仮定):　t=', t_welch[0], ', p=', t_welch[1], ',  jud: ', t_welch[2],
                              sep='')

        elif is_rel == 'n':
                t_stu_rel_result = ttest_student_rel(df1, df2)
                print('関連2群のt検定(等分散・正規分布を仮定):　t=', t_stu_rel_result[0], ', p=', t_stu_rel_result[1], ',  jud: ',
                      t_stu_rel_result[2], sep='')

else:
        leve_result = variance_levene(df1, df2)
        print('Levene検定(非正規分布を仮定): W=', leve_result[0], ', p=', leve_result[1], ',  jud: ', leve_result[2], sep='')
        variance = leve_result[1]

        if is_rel == 'y':
                mann_result = mann(df1 ,df2)
                print('Mann-Whitney検定(独立2群・非正規分布を仮定): W=', leve_result[0], ', p=', leve_result[1], ',  jud: ', leve_result[2], sep='')

        elif is_rel == 'n':
                wilc_result = wilcoxon_signed(df1, df2)
                print('Wilcoxon Signed-rank検定(関連2群・非正規分布を仮定): W=', wilc_result[0], ', p=', wilc_result[1], ',  jud: ', wilc_result[2], sep='')


avg_df1 = np.mean(listize(df1))
avg_df2 = np.mean(listize(df2))

print(df1_name, ': M=', avg_df1, ', SD=', stdev(listize(df1)), sep='')
print(df2_name, ': M=', avg_df2, ', SD=', stdev(listize(df2)), sep='')
