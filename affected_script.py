import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

EXPERIMENT_NAME = '가설2번'
#DAY_LENGTH = 25
DAY_LENGTH = 37

path = 'result/csv/' + EXPERIMENT_NAME
all_files = glob.glob(os.path.join(path, "*.csv"))

df_from_each_file = [pd.read_csv(f) for f in all_files]

df_from_each_file[0].rename(columns={'Unnamed: 0': 'step'}, inplace=True)
result = df_from_each_file[0].drop(['Infected', 'Recovered', 'Exposed'], axis=1)
result.rename(columns={'Unnamed: 0': 'step'}, inplace=True)
#
# for x in range(1, len(df_from_each_file)):
#         k += r
#
#     df_from_each_file[x] = df_from_each_file[x].drop(['Infected', 'Recovered', 'Exposed'], axis=1)
#     df_from_each_file[x].rename(columns={'Unnamed: 0': 'step'}, inplace=True)
#     result = pd.merge(df_from_each_file[x], result, on='step')
#
#
# result.to_csv(EXPERIMENT_NAME + 'susceptible.csv')
# 엑셀에서 평균 구하기

cnt = 100000
for x in df_from_each_file:
    a = len(x.Susceptible.index)
    if a < cnt:
        cnt = len(x.Susceptible.index)
k = []


for y in range(1, cnt, DAY_LENGTH):
    r = 0
    a = 0
    for t in df_from_each_file:
        # if type(t.iloc[y, 1]) != int:
        #     break
        r += 1050 - t.iloc[y, 1]
        a += 1
    r = r / a
    k.append(r)

final = pd.DataFrame(data=k, index=range(cnt // DAY_LENGTH + 1))
final.to_csv('result/average/' + EXPERIMENT_NAME + '_infected_average.csv')
final.plot()
plt.xlim(0,40)
plt.savefig('result/average/' + EXPERIMENT_NAME + '_infected_average_xlim.png', bbox_inches='tight')
plt.close()