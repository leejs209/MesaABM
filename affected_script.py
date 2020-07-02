import pandas as pd
import glob
import os

EXPERIMENT_NAME = '가설1번'
path = 'result/csv/' + EXPERIMENT_NAME
all_files = glob.glob(os.path.join(path, "*.csv"))

df_from_each_file = [pd.read_csv(f) for f in all_files]

# df_from_each_file[0].rename(columns={'Unnamed: 0': 'step'}, inplace=True)
result = df_from_each_file[0].drop(['Infected', 'Recovered', 'Exposed'], axis=1)
result.rename(columns={'Unnamed: 0': 'step'}, inplace=True)
for x in range(1, len(df_from_each_file)):
    df_from_each_file[x] = df_from_each_file[x].drop(['Infected', 'Recovered', 'Exposed'], axis=1)
    df_from_each_file[x].rename(columns={'Unnamed: 0': 'step'}, inplace=True)
    result = pd.merge(df_from_each_file[x], result, on='step')

result.to_csv(EXPERIMENT_NAME + 'susceptible.csv')

#엑셀에서 평균 구하기