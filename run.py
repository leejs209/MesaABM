from mesa.visualization.ModularVisualization import ModularServer
from MesaABM.model import SchoolModel
from MesaABM.visualization import grid, s_chart

server = ModularServer(SchoolModel,
                       [grid, s_chart],
                       "School Model",
                       {"N": 1050, "N_per_group": 25, "width": 140, "height": 60,
                        "initial_num_infected": 1, "infection_duration": 30, "infection_prob_per_contact": 0.2,
                        "restaurant_multiplier": 3, "visit_prob_per_person": 0.4})
server.port = 8080
server.launch()