from MesaABM.model import SchoolModel
from matplotlib import pyplot as plt
import datetime
import time

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

model = SchoolModel(N=1050, N_per_group=25, width=140, height=61, initial_num_infected=1,
                    infection_duration=7, exposed_duration=5,
                    infection_prob_per_contact=0.2, exposed_infection_prob_per_contact=0.1,
                    restaurant_multiplier=3, visit_prob_per_person=0.3,
                    meal_random=True, meal_distanced=False, dinner_percentage=0.3,
                    timetable=timetable_extra, split_opening=False)

start = time.time()
model.step()
while model.i_count != 0 or model.e_count != 0:
    model.step()
asdf = str(datetime.datetime.now().strftime('%m-%d %H-%M-%S'))
result = model.datacollector.get_model_vars_dataframe()
result.plot()
plt.savefig('대조군' + asdf + '.png', bbox_inches='tight')
result.to_csv(asdf + '.csv')

r = '\n'
for x in range(4):
    r = r + str(result.iloc[7 * len(model.timetable)][x]) + ','

r += str(model.step_no) + ','

end = time.time()
print(str(end - start) + '초 소요됨')

r += str(end - start)
with open('대조군.csv','a') as f:
    f.write(r)