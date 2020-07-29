from MesaABM.model import SchoolModel
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import time
import glob
import os

# 그래프 출력 한글폰트 지원, OS에 따라 수정하기
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
plt.rc('font', family=font_name)

timetable_normal = [
    'recess',
    'recess_cont',
    'recess',
    'recess_cont',
    'recess',
    'recess_cont',
    'recess',
    'recess_cont',
    'recess',
    'recess_cont',
    'recess',
    'recess_cont',
    'meal',
    'meal_cont',
    'meal_cont',
    'recess',
    'recess_cont',
    'recess_cont',
    'recess_cont',
    'recess_cont',
    'recess_cont',
    'recess',
    'recess_cont',
    'recess',
    'recess_cont'
]

timetable_extra = timetable_normal + [
    'recess',
    'recess_cont',
    'recess',
    'recess_cont',
    'dinner',
    'dinner_cont',
    'dinner_cont',
    'recess',
    'recess_cont',
    'recess_cont',
    'recess_cont',
    'recess_cont',
    'recess_cont',
    'recess_cont'
]

RESULT_DIR = "result/"  # 출력 폴더. "/"로 끝나야 한다.
STUDENT_NO = 1050  # 총 학생 수

def do_experiment(EXPERIMENT_NAME, split_opening, extra_school, visit_prob_per_person, meal_random):
    """ RESULT_DIR/csv/EXPERIMENT_NAME라는 폴더에 실험 실행 결과의 csv 파일을 저장한다."""
    timetable = timetable_normal
    if extra_school:
        timetable = timetable_extra

    # 모델에 적절한 인자를 대입한다.
    model = SchoolModel(N=STUDENT_NO, N_per_group=25, width=140, height=61, initial_num_infected=1,
                        infection_duration=7, exposed_duration=5,
                        infection_prob_per_contact=0.2, exposed_infection_prob_per_contact=0.05,
                        restaurant_multiplier=3, visit_prob_per_person=visit_prob_per_person,
                        meal_random=meal_random, meal_distanced=False, dinner_percentage=0.3,
                        timetable=timetable, split_opening=split_opening)

    datetime_string = str(datetime.datetime.now().strftime('%m-%d %H-%M-%S'))
    start = time.time()  # 모델 실행에 걸리는 시간을 측정한다.
    model.step()
    while model.i_count != 0 or model.e_count != 0:  # 감염자 또는 잠복기가 0명이 될 때까지 측정한다.
        model.step()

    result = model.datacollector.get_model_vars_dataframe()
    # 실험 실행 후 결과를 그래프로 그려 RESULT_DIR에 이미지 파일로 저장한다.
    # result.plot()
    # plt.xlim(0, 2000)
    # plt.savefig(RESULT_DIR + EXPERIMENT_NAME + datetime_string + '.png', bbox_inches='tight')
    # plt.close()

    # csv 파일로 실험 결과를 출력한다.
    if not os.path.exists(RESULT_DIR + 'csv'):
        os.mkdir(RESULT_DIR + 'csv')
    if not os.path.exists(RESULT_DIR + 'csv/' + EXPERIMENT_NAME):
        os.mkdir(RESULT_DIR + 'csv/' + EXPERIMENT_NAME)

    result.to_csv(RESULT_DIR + 'csv/' + EXPERIMENT_NAME + '/' + EXPERIMENT_NAME + datetime_string + '.csv')

    # result라는 이름의 Dataframe에서 4개의 column에 대해 7일(7 * 1일당 step 수)이 흐른 후의 값들을 EXPERIMET_NAME.csv에 추가한다.
    # r = '\n'
    #
    # for x in range(4):
    #     r = r + str(result.iloc[7 * len(model.timetable)][x]) + ','
    #
    # r += str(model.step_no) + ','
    # with open(RESULT_DIR + EXPERIMENT_NAME + '.csv', 'a') as f:
    #     f.write(r)
    #     f.close()

    # 소요 시간 출력
    end = time.time()
    print(EXPERIMENT_NAME + ": " + str(end - start) + '초 소요됨')

def average_IER(EXPERIMENT_NAME, DAY_LENGTH):
    """ RESULT_DIR/csv에서 인자로 받은 EXPERIMENT_NAME라는 이름을 가진 폴더의 csv 파일들의 평균을 구하여 RESULT_DIR/average에 저장한다."""

    if not os.path.exists(RESULT_DIR + 'average'):
        os.mkdir(RESULT_DIR + 'average')
    # DAY_LENGTH = 25
    # DAY_LENGTH = 37

    # do_experiment에서 출력한 실험의 결과를 모두 불러온다.
    path = RESULT_DIR + 'csv/' + EXPERIMENT_NAME
    all_files = glob.glob(os.path.join(path, "*.csv"))
    df_from_each_file = [pd.read_csv(f) for f in all_files]

    # 불러온 파일 중 첫번째 파일의 column 이름을 적절히 바꾸고 I, R, E에 해당하는 column을 삭제한다.
    # df_from_each_file[0].rename(columns={'Unnamed: 0': 'step'}, inplace=True)
    # result = df_from_each_file[0].drop(['Infected', 'Recovered', 'Exposed'], axis=1)
    # result.rename(columns={'Unnamed: 0': 'step'}, inplace=True)

    # 실험 결과 파일 중 step 수가 가장 짧은 값을 구한다.
    cnt = float('inf')
    for x in df_from_each_file:
        a = len(x.Susceptible.index)
        if a < cnt:
            cnt = len(x.Susceptible.index)

    # 불러온 실험들의 각 행에 대해 (전체 인구 - S값)의 평균을 구하고 k 리스트에 추가한다..
    k = []
    for y in range(1, cnt, DAY_LENGTH):
        r = 0
        a = 0
        for t in df_from_each_file:
            r += STUDENT_NO - t.iloc[y, 1]
            a += 1
        r = r / a
        k.append(r)

    # x축을 경과 시간으로, y축을 (전체 - S)의 인구수의 값으로 하여 Dataframe을 출력한다.
    final = pd.DataFrame(data=k, index=range(cnt // DAY_LENGTH + 1))
    final.to_csv(RESULT_DIR + 'average/' + EXPERIMENT_NAME + '_infected_average.csv')

    # 각 실험의 평균 값을 그래프로 출력한다.
    # final.plot()
    # plt.xlim(0, 40)
    # plt.savefig(RESULT_DIR + 'average/' + EXPERIMENT_NAME + '_infected_average_xlim.png', bbox_inches='tight')
    # plt.close()

def combine_averages():
    """ 실험 결과를 평균처리 한 파일을 하나의 dataframe으로 합치고 그래프를 출력한다. """
    # average 폴더의 csv 파일을 모두 불러온다
    path = RESULT_DIR + 'average'
    all_files = glob.glob(os.path.join(path, "*.csv"))
    df_from_each_file = [pd.read_csv(f) for f in all_files]

    # average 폴더에서 불러온 첫 파일을 템플릿으로 삼고, csv 파일 이름을 column 이름으로 한다.
    final = df_from_each_file[0]
    final.rename(columns={'0': os.path.basename(list(all_files)[0])}, inplace=True)

    # average 폴더의 나머지 파일에서 IER 합친 값을 불러온 후 final Dataframe에 추가한다.
    for t in range(1, len(df_from_each_file)):
        x = df_from_each_file[t]
        x.rename(columns={'0': os.path.basename(list(all_files)[t])}, inplace=True)
        t += 1
        final = pd.merge(final, x, on='Unnamed: 0')

    # 마무리 작업으로 step column을 제거한다.
    final.drop(['Unnamed: 0'], axis=1, inplace=True)

    # 최종적으로 합친 값을 출력한다.
    final.to_csv(RESULT_DIR + 'average/infected_average.csv')

    # 그래프로 출력한다.
    final.plot()
    plt.xlim(0, 40)
    plt.savefig(RESULT_DIR + 'average/infected_average_xlim.png', bbox_inches='tight')
    plt.close()

def combine_same_hypothesis(EXPERIMENT_NAME):
    path = RESULT_DIR + 'csv/' + EXPERIMENT_NAME
    all_files = glob.glob(os.path.join(path, "*.csv"))

    df_from_each_file = [pd.read_csv(f) for f in all_files]

    # 첫번쨰 파일을 탬플릿으로
    final = df_from_each_file[0]
    final.drop(["Infected", 'Recovered', 'Exposed'], axis=1, inplace=True)
    final.rename(columns={'Susceptible': os.path.basename(list(all_files)[0])}, inplace=True)

    # 여러 실험을 한 dataframe으로 합치기
    for t in range(1, len(df_from_each_file)):
        x = df_from_each_file[t]
        x.drop(["Infected", 'Recovered', 'Exposed'], axis=1, inplace=True)
        x.rename(columns={'Susceptible': os.path.basename(list(all_files)[t])}, inplace=True)
        t += 1
        final = pd.merge(final, x, on='Unnamed: 0')

    # 필요없는 step column 지우기
    final.drop(['Unnamed: 0'], axis=1, inplace=True)

    if not os.path.exists(RESULT_DIR + 'total'):
        os.mkdir(RESULT_DIR + 'total')
    final.to_csv(RESULT_DIR + 'total/' + EXPERIMENT_NAME + '_EIR_combined.csv')
    final.plot(legend=None)
    plt.xlim(0, 2000)
    plt.savefig(RESULT_DIR + 'total/' + EXPERIMENT_NAME + '_EIR_combined_xlim.png', bbox_inches='tight')
    plt.close()

# for t in range(30):
#     print(str(t+1) + "번쨰 실험")
#     do_experiment('대조군', False, False, 0.1, True)
#     do_experiment('가설1번', True, False, 0.1, True)
#     do_experiment('가설2번', False, True, 0.1, True)
#     do_experiment('가설3번', False, False, 0, True)
#     do_experiment('가설4번', False, False, 0.1, False)

average_IER('대조군', 25)
average_IER('가설1번', 25)
average_IER('가설2번', 37)
average_IER('가설3번', 25)
average_IER('가설4번', 25)

experiments = ['대조군', '가설 1번', '가설 2번', '가설 3번', '가설 4번']
for ex in experiments:
    combine_same_hypothesis(ex)

combine_averages()