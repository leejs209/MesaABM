
from mesa.visualization.ModularVisualization import ModularServer
from MesaABM.model import SchoolModel
from MesaABM.visualization import grid


server = ModularServer(SchoolModel,
                       [grid],
                       "School Model",
                       {"N": 100, "group_N": 10, "width": 50, "height": 50, "initial_num_infected": 1})
server.port = 8080
server.launch()