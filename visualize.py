from mesa.visualization.ModularVisualization import ModularServer
from MesaABM.model import SchoolModel
from MesaABM.visualization import grid, s_chart
import asyncio

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

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
server = ModularServer(SchoolModel,
                       [grid, s_chart],
                       "School Model",
                       {"N": 1050, "N_per_group": 25, "width": 140, "height": 61,
                        "initial_num_infected": 1, "infection_duration": 7,  "exposed_duration": 5,
                        "infection_prob_per_contact": 0.2, "exposed_infection_prob_per_contact": 0.1,
                        "restaurant_multiplier": 3, "visit_prob_per_person": 0.1,
                        "meal_random": False, "meal_distanced": False, "dinner_percentage": 0.3,
                        "timetable": timetable_normal, "split_opening": False})

server.port = 8082
server.launch()