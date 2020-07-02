from MesaABM.model import SchoolModel
from matplotlib import pyplot as plt
import datetime
import time
from mesa.batchrunner import BatchRunner
import os.path

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



def do_experiment(EXPERIMENT_NAME, split_opening, extra_school, visit_prob_per_person, meal_random):
    timetable = timetable_normal
    if extra_school:
        timetable = timetable_extra

    model = SchoolModel(N=1050, N_per_group=25, width=140, height=61, initial_num_infected=1,
                        infection_duration=7, exposed_duration=5,
                        infection_prob_per_contact=0.2, exposed_infection_prob_per_contact=0.05,
                        restaurant_multiplier=3, visit_prob_per_person=visit_prob_per_person,
                        meal_random=meal_random, meal_distanced=False, dinner_percentage=0.3,
                        timetable=timetable, split_opening=split_opening)
    start = time.time()
    model.step()
    while model.i_count != 0 or model.e_count != 0:
        model.step()
    asdf = str(datetime.datetime.now().strftime('%m-%d %H-%M-%S'))

    result = model.datacollector.get_model_vars_dataframe()
    result.plot()
    plt.xlim(0, 2000)
    plt.savefig('result/' + EXPERIMENT_NAME + asdf + '.png', bbox_inches='tight')
    plt.close()

    result.to_csv('result/csv/' + EXPERIMENT_NAME + '/' + EXPERIMENT_NAME + asdf + '.csv')

    r = '\n'
    for x in range(4):
        r = r + str(result.iloc[7 * len(model.timetable)][x]) + ','

    r += str(model.step_no) + ','

    end = time.time()
    print(EXPERIMENT_NAME + ": " + str(end - start) + '초 소요됨')

    r += str(end - start)
    with open('result/' + EXPERIMENT_NAME + '.csv', 'a') as f:
        f.write(r)
        f.close()


# do_experiment(EXPERIMENT_NAME, split_opening, extra_school, visit_prob_per_person, meal_random):
for _ in range(1000):
    #do_experiment('대조군', False, False, 0.1, True)
#for _ in range(5):
    do_experiment('가설1번', True, False, 0.1, True)
#for _ in range(5):
    #do_experiment('가설2번', False, True, 0.1, True)
#for _ in range(0):
    #do_experiment('가설3번', False, False, 0, True)
#for _ in range(0):
    #do_experiment('가설4번', False, False, 0.1, False)