import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
plt.rc('font', family=font_name)

EXPERIMENT_NAME = '가설4번'
path = 'result/csv/' + EXPERIMENT_NAME
all_files = glob.glob(os.path.join(path, "*.csv"))

df_from_each_file = [pd.read_csv(f) for f in all_files]

# cnt = 100000
# for x in df_from_each_file:
#     a = len(x.index)
#     if a < cnt:
#         cnt = len(x.index)
#
# result = []
# for x in df_from_each_file:
#     result.append(x.iloc)
#
# final = pd.DataFrame(data=, index=range(cnt))
t = 0
final = df_from_each_file[0]
final.drop(["Infected", 'Recovered', 'Exposed'], axis=1, inplace=True)
final.rename(columns={'Susceptible': os.path.basename(list(all_files)[0])}, inplace=True)
for t in range(1, len(df_from_each_file)):
    x = df_from_each_file[t]
    x.drop(["Infected", 'Recovered', 'Exposed'], axis=1, inplace=True)
    x.rename(columns={'Susceptible': os.path.basename(list(all_files)[t])}, inplace=True)
    t += 1
    final = pd.merge(final, x, on='Unnamed: 0')
final.drop(['Unnamed: 0'], axis=1, inplace=True)
final.to_csv('result/average/infected_average.csv')
final.plot(legend=None)
plt.xlim(0, 2000)
plt.savefig('result/total/' + EXPERIMENT_NAME + '_infected_average_xlim.png', bbox_inches='tight')
plt.close()
