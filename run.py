from mesa.visualization.ModularVisualization import ModularServer
from MesaABM.model import SchoolModel
from MesaABM.visualization import grid, s_chart

server = ModularServer(SchoolModel,
                       [grid, s_chart],
                       "School Model",
                       {"N": 1000, "group_N": 10, "width": 50, "height": 50,
                        "initial_num_infected": 1, "infection_duration": 30})
server.port = 8080
server.launch()